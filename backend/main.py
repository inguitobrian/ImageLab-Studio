"""
FastAPI Backend for OpenCV Image Processing Studio
Vue.js Frontend Compatible Version
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import json
from typing import List, Optional
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OpenCV Processing Studio API", 
    version="1.0.0",
    description="Professional OpenCV Image Processing with Vue.js Frontend Support"
)

# Enable CORS for Vue.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# Helper functions
def decode_base64_image(base64_string: str) -> np.ndarray:
    """Convert base64 string to OpenCV image"""
    try:
        # Remove data URL prefix if present
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_string)
        
        # Convert to PIL Image then to OpenCV format
        pil_image = Image.open(BytesIO(image_data))
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return opencv_image
    except Exception as e:
        logger.error(f"Error decoding base64 image: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

def encode_image_to_base64(image: np.ndarray) -> str:
    """Convert OpenCV image to base64 string"""
    try:
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(image_rgb)
        
        # Convert to base64
        buffer = BytesIO()
        pil_image.save(buffer, format='PNG')
        
        return base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
        logger.error(f"Error encoding image to base64: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OpenCV Image Processing Studio API", 
        "status": "running",
        "frontend": "Vue.js",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "opencv_version": cv2.__version__,
        "api_version": "1.0.0"
    }


#GETTING STARTED


@app.post("/api/load-image")
async def load_image(file: UploadFile = File(...)):
    """Load and return image information"""
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        height, width, channels = image.shape
        
        return {
            "width": int(width),
            "height": int(height),
            "channels": int(channels),
            "size": len(contents),
            "format": file.content_type,
            "image": encode_image_to_base64(image),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error loading image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dimensions")
async def get_dimensions(image_data: str = Form(...)):
    """Get image dimensions and properties"""
    try:
        image = decode_base64_image(image_data)
        height, width = image.shape[:2]
        channels = image.shape[2] if len(image.shape) == 3 else 1
        
        return {
            "width": int(width),
            "height": int(height),
            "channels": int(channels),
            "total_pixels": int(width * height),
            "data_type": str(image.dtype),
            "operation": "dimensions_check"
        }
    except Exception as e:
        logger.error(f"Error getting dimensions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# GRAYSCALING


@app.post("/api/grayscale")
async def convert_grayscale(image_data: str = Form(...)):
    """Convert image to grayscale"""
    try:
        image = decode_base64_image(image_data)
        
        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Convert back to 3-channel for consistent display
        gray_3channel = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        
        return {
            "processed_image": encode_image_to_base64(gray_3channel),
            "original_shape": image.shape,
            "processed_shape": gray_image.shape,
            "operation": "grayscale_conversion"
        }
    except Exception as e:
        logger.error(f"Error in grayscale conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compare-dimensions")
async def compare_dimensions(image_data: str = Form(...)):
    """Compare color and grayscale image dimensions"""
    try:
        image = decode_base64_image(image_data)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        return {
            "color_dimensions": {
                "height": image.shape[0],
                "width": image.shape[1],
                "channels": image.shape[2],
                "total_size": image.size
            },
            "grayscale_dimensions": {
                "height": gray_image.shape[0],
                "width": gray_image.shape[1],
                "channels": 1,
                "total_size": gray_image.size
            },
            "size_reduction": f"{((image.size - gray_image.size) / image.size * 100):.1f}%",
            "operation": "dimension_comparison"
        }
    except Exception as e:
        logger.error(f"Error comparing dimensions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# COLOR SPACES  


@app.post("/api/rgb-channels")
async def extract_rgb_channels(image_data: str = Form(...)):
    """Extract individual RGB channels"""
    try:
        image = decode_base64_image(image_data)
        
        # Split into BGR channels (OpenCV uses BGR)
        b, g, r = cv2.split(image)
        
        # Create single-channel visualizations
        b_3channel = cv2.merge([b, np.zeros_like(b), np.zeros_like(b)])
        g_3channel = cv2.merge([np.zeros_like(g), g, np.zeros_like(g)])
        r_3channel = cv2.merge([np.zeros_like(r), np.zeros_like(r), r])
        
        return {
            "red_channel": encode_image_to_base64(r_3channel),
            "green_channel": encode_image_to_base64(g_3channel),
            "blue_channel": encode_image_to_base64(b_3channel),
            "operation": "rgb_channel_extraction"
        }
    except Exception as e:
        logger.error(f"Error extracting RGB channels: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/hsv-convert")
async def convert_hsv(image_data: str = Form(...)):
    """Convert image to HSV color space"""
    try:
        image = decode_base64_image(image_data)
        
        # Convert to HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Split HSV channels
        h, s, v = cv2.split(hsv_image)
        
        # Create visualizations
        h_vis = cv2.applyColorMap(h, cv2.COLORMAP_HSV)
        s_vis = cv2.cvtColor(s, cv2.COLOR_GRAY2BGR)
        v_vis = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)
        
        return {
            "hsv_image": encode_image_to_base64(cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)),
            "hue_channel": encode_image_to_base64(h_vis),
            "saturation_channel": encode_image_to_base64(s_vis),
            "value_channel": encode_image_to_base64(v_vis),
            "operation": "hsv_conversion"
        }
    except Exception as e:
        logger.error(f"Error in HSV conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/color-manipulation")
async def manipulate_color(
    image_data: str = Form(...),
    hue_shift: int = Form(0),
    saturation_factor: float = Form(1.0),
    value_factor: float = Form(1.0)
):
    """Manipulate color channels"""
    try:
        image = decode_base64_image(image_data)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Manipulate HSV channels
        hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_shift) % 180
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 255)
        hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * value_factor, 0, 255)
        
        # Convert back to BGR
        result_image = cv2.cvtColor(hsv_image.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "hue_shift": hue_shift,
            "saturation_factor": saturation_factor,
            "value_factor": value_factor,
            "operation": "color_manipulation"
        }
    except Exception as e:
        logger.error(f"Error in color manipulation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


#DRAWING AND SHAPES

# ...existing code...

@app.post("/api/draw-shapes")
async def draw_shapes(
    image_data: str = Form(...),
    shapes: str = Form(default="[]")
):
    """Draw user-defined shapes on image"""
    try:
        import json
        image = decode_base64_image(image_data)
        height, width = image.shape[:2]
        
        # Create a copy to draw on
        result_image = image.copy()
        
        # Parse shapes from JSON
        try:
            shapes_list = json.loads(shapes) if shapes else []
            logger.info(f"Processing {len(shapes_list)} shapes")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            shapes_list = []
        
        drawn_shapes = []
        
        for i, shape in enumerate(shapes_list):
            logger.info(f"Processing shape {i}: {shape}")
            
            shape_type = shape.get("type", "").lower()
            color = shape.get("color", [255, 255, 255])
            thickness = shape.get("thickness", 2)
            filled = shape.get("filled", False)
            
            # Validate color format
            if not isinstance(color, list) or len(color) < 3:
                logger.warning(f"Invalid color format: {color}, using default")
                color = [255, 255, 255]
            
            # Validate thickness
            try:
                thickness = int(thickness)
                if thickness < 1:
                    thickness = 1
            except (ValueError, TypeError):
                logger.warning(f"Invalid thickness: {thickness}, using default")
                thickness = 2
            
            # Convert RGB to BGR for OpenCV
            bgr_color = (int(color[2]), int(color[1]), int(color[0]))
            line_thickness = -1 if filled else thickness
            
            try:
                if shape_type == "rectangle":
                    # Get and validate coordinates
                    x1 = int(shape.get("x1", 0))
                    y1 = int(shape.get("y1", 0))  
                    x2 = int(shape.get("x2", 100))
                    y2 = int(shape.get("y2", 100))
                    
                    # Ensure coordinates are within image bounds
                    x1 = max(0, min(x1, width - 1))
                    y1 = max(0, min(y1, height - 1))
                    x2 = max(0, min(x2, width - 1))
                    y2 = max(0, min(y2, height - 1))
                    
                    # Ensure we have a valid rectangle (not just a line)
                    if abs(x2 - x1) > 0 and abs(y2 - y1) > 0:
                        cv2.rectangle(result_image, (x1, y1), (x2, y2), bgr_color, line_thickness)
                        drawn_shapes.append(f"Rectangle: ({x1},{y1}) to ({x2},{y2})")
                    else:
                        logger.warning(f"Invalid rectangle dimensions: ({x1},{y1}) to ({x2},{y2})")
                        
                elif shape_type == "circle":
                    center_x = int(shape.get("center_x", 50))
                    center_y = int(shape.get("center_y", 50))
                    radius = int(shape.get("radius", 25))
                    
                    # Validate parameters
                    center_x = max(0, min(center_x, width - 1))
                    center_y = max(0, min(center_y, height - 1))
                    radius = max(1, min(radius, min(width, height) // 2))
                    
                    cv2.circle(result_image, (center_x, center_y), radius, bgr_color, line_thickness)
                    drawn_shapes.append(f"Circle: center({center_x},{center_y}), radius={radius}")
                    
                elif shape_type == "ellipse":
                    center_x = int(shape.get("center_x", 50))
                    center_y = int(shape.get("center_y", 50))
                    width_axis = int(shape.get("width", 50))
                    height_axis = int(shape.get("height", 30))
                    angle = float(shape.get("angle", 0))
                    start_angle = float(shape.get("start_angle", 0))
                    end_angle = float(shape.get("end_angle", 360))
                    
                    # Validate parameters
                    center_x = max(0, min(center_x, width - 1))
                    center_y = max(0, min(center_y, height - 1))
                    width_axis = max(1, width_axis)
                    height_axis = max(1, height_axis)
                    
                    cv2.ellipse(result_image, (center_x, center_y), (width_axis, height_axis), 
                               angle, start_angle, end_angle, bgr_color, line_thickness)
                    drawn_shapes.append(f"Ellipse: center({center_x},{center_y}), axes({width_axis},{height_axis})")
                    
                elif shape_type == "line":
                    x1 = int(shape.get("x1", 0))
                    y1 = int(shape.get("y1", 0))
                    x2 = int(shape.get("x2", 100))
                    y2 = int(shape.get("y2", 100))
                    
                    # Validate coordinates
                    x1 = max(0, min(x1, width - 1))
                    y1 = max(0, min(y1, height - 1))
                    x2 = max(0, min(x2, width - 1))
                    y2 = max(0, min(y2, height - 1))
                    
                    cv2.line(result_image, (x1, y1), (x2, y2), bgr_color, thickness)
                    drawn_shapes.append(f"Line: ({x1},{y1}) to ({x2},{y2})")
                    
                elif shape_type == "polygon":
                    polygon_type = shape.get("polygon_type", "pentagon")
                    center_x = int(shape.get("center_x", 150))
                    center_y = int(shape.get("center_y", 150))
                    size = int(shape.get("size", 80))
                    
                    # Validate center coordinates
                    center_x = max(size, min(center_x, width - size))
                    center_y = max(size, min(center_y, height - size))
                    
                    try:
                        # Generate predefined polygon points based on type
                        if polygon_type == "triangle":
                            # Equilateral triangle
                            points = [
                                [center_x, center_y - size],              # Top
                                [center_x - int(size * 0.866), center_y + size//2],  # Bottom left
                                [center_x + int(size * 0.866), center_y + size//2]   # Bottom right
                            ]
                        else:
                            # Default to pentagon
                            points = []
                            for i in range(5):
                                angle = i * 2 * 3.14159 / 5 - 3.14159/2
                                x = int(center_x + size * np.cos(angle))
                                y = int(center_y + size * np.sin(angle))
                                points.append([x, y])
                        
                        # Ensure all points are within image bounds
                        valid_points = []
                        for point in points:
                            x = max(0, min(point[0], width - 1))
                            y = max(0, min(point[1], height - 1))
                            valid_points.append([x, y])
                        
                        # Let's define the points using numpy array
                        pts_original = np.array(valid_points, np.int32)
                        
                        if filled:
                            cv2.fillPoly(result_image, [pts_original], bgr_color)
                            drawn_shapes.append(f"Filled {polygon_type.title()}: center({center_x},{center_y})")
                        else:
                            # Let's now reshape our points in form required by polylines
                            pts_reshaped = pts_original.reshape((-1, 1, 2))
                            cv2.polylines(result_image, [pts_reshaped], True, bgr_color, thickness)
                            drawn_shapes.append(f"{polygon_type.title()} Outline: center({center_x},{center_y})")
                            
                    except (ValueError, TypeError) as poly_error:
                        logger.error(f"Polygon processing error: {poly_error}")
                        continue
                        
                elif shape_type == "arrow":
                    x1 = int(shape.get("x1", 0))
                    y1 = int(shape.get("y1", 0))
                    x2 = int(shape.get("x2", 100))
                    y2 = int(shape.get("y2", 100))
                    tip_length = float(shape.get("tip_length", 0.1))
                    
                    # Validate coordinates
                    x1 = max(0, min(x1, width - 1))
                    y1 = max(0, min(y1, height - 1))
                    x2 = max(0, min(x2, width - 1))
                    y2 = max(0, min(y2, height - 1))
                    
                    # Validate tip_length
                    tip_length = max(0.05, min(tip_length, 0.5))
                    
                    cv2.arrowedLine(result_image, (x1, y1), (x2, y2), bgr_color, thickness, tipLength=tip_length)
                    drawn_shapes.append(f"Arrow: ({x1},{y1}) to ({x2},{y2})")
                    
                else:
                    logger.warning(f"Unknown shape type: {shape_type}")
                    continue
                    
            except Exception as shape_error:
                logger.error(f"Error drawing {shape_type}: {shape_error}")
                logger.error(f"Shape data: {shape}")
                continue
        
        logger.info(f"Successfully drew {len(drawn_shapes)} shapes")
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "shapes_drawn": drawn_shapes,
            "total_shapes": len(drawn_shapes),
            "operation": "draw_custom_shapes"
        }
        
    except Exception as e:
        logger.error(f"Error in draw_shapes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Drawing error: {str(e)}")

@app.post("/api/draw-freehand")
async def draw_freehand(
    image_data: str = Form(...),
    points: str = Form(...),  # JSON array of {x, y} coordinates
    color: str = Form(default="[255, 255, 255]"),  # RGB color as JSON
    thickness: int = Form(default=2),
    closed: bool = Form(default=False)
):
    """Draw freehand lines/curves from array of points"""
    try:
        import json
        image = decode_base64_image(image_data)
        result_image = image.copy()
        
        # Parse points and color
        points_list = json.loads(points)
        color_rgb = json.loads(color)
        bgr_color = (int(color_rgb[2]), int(color_rgb[1]), int(color_rgb[0]))
        
        if len(points_list) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 points to draw")
        
        # Convert points to numpy array
        pts = np.array([[int(p["x"]), int(p["y"])] for p in points_list], np.int32)
        
        if closed:
            # Draw closed polygon
            cv2.polylines(result_image, [pts], True, bgr_color, thickness)
        else:
            # Draw connected lines
            for i in range(len(pts) - 1):
                cv2.line(result_image, tuple(pts[i]), tuple(pts[i + 1]), bgr_color, thickness)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "points_count": len(points_list),
            "closed": closed,
            "operation": "draw_freehand"
        }
    except Exception as e:
        logger.error(f"Error drawing freehand: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/draw-text-custom")
async def draw_text_custom(
    image_data: str = Form(...),
    text_elements: str = Form(default="[]")  # JSON array of text objects
):
    """Draw multiple custom text elements"""
    try:
        import json
        image = decode_base64_image(image_data)
        result_image = image.copy()
        
        # Parse text elements
        texts = json.loads(text_elements) if text_elements else []
        drawn_texts = []
        
        for text_elem in texts:
            try:
                text = text_elem.get("text", "Sample Text")
                x, y = int(text_elem.get("x", 50)), int(text_elem.get("y", 50))
                font_scale = float(text_elem.get("font_scale", 1.0))
                color = text_elem.get("color", [255, 255, 255])
                thickness = int(text_elem.get("thickness", 2))
                font_name = text_elem.get("font", "HERSHEY_SIMPLEX")
                
                # Map font names to OpenCV constants
                font_map = {
                    "HERSHEY_SIMPLEX": cv2.FONT_HERSHEY_SIMPLEX,
                    "HERSHEY_PLAIN": cv2.FONT_HERSHEY_PLAIN,
                    "HERSHEY_DUPLEX": cv2.FONT_HERSHEY_DUPLEX,
                    "HERSHEY_COMPLEX": cv2.FONT_HERSHEY_COMPLEX,
                    "HERSHEY_TRIPLEX": cv2.FONT_HERSHEY_TRIPLEX,
                    "HERSHEY_COMPLEX_SMALL": cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    "HERSHEY_SCRIPT_SIMPLEX": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    "HERSHEY_SCRIPT_COMPLEX": cv2.FONT_HERSHEY_SCRIPT_COMPLEX
                }
                
                font = font_map.get(font_name, cv2.FONT_HERSHEY_SIMPLEX)
                bgr_color = (int(color[2]), int(color[1]), int(color[0])) if len(color) >= 3 else (255, 255, 255)
                
                h, w = result_image.shape[:2]
                (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
                x = (w - text_width) // 2
                y = (h + text_height) // 2
                
                cv2.putText(result_image, text, (x, y), font, font_scale, bgr_color, thickness)
                drawn_texts.append(f"Text: '{text}' at ({x},{y})")
                
            except (KeyError, ValueError, TypeError) as e:
                logger.warning(f"Skipping invalid text element: {str(e)}")
                continue
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "texts_drawn": drawn_texts,
            "total_texts": len(drawn_texts),
            "operation": "draw_custom_text"
        }
    except Exception as e:
        logger.error(f"Error drawing custom text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# TRANSFORMATIONS


@app.post("/api/translate")
async def translate_image(
    image_data: str = Form(...),
    tx: int = Form(50),
    ty: int = Form(50)
):
    """Translate (move) image"""
    try:
        image = decode_base64_image(image_data)
        height, width = image.shape[:2]
        
        # Create translation matrix
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        
        # Apply translation
        translated_image = cv2.warpAffine(image, M, (width, height))
        
        return {
            "processed_image": encode_image_to_base64(translated_image),
            "translation_x": tx,
            "translation_y": ty,
            "operation": "translation"
        }
    except Exception as e:
        logger.error(f"Error in translation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rotate")
async def rotate_image(
    image_data: str = Form(...),
    angle: float = Form(45.0),
    scale: float = Form(1.0)
):
    """Rotate image using getRotationMatrix2D"""
    try:
        image = decode_base64_image(image_data)
        height, width = image.shape[:2]
        
        # Get rotation matrix
        center = (width // 2, height // 2)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        
        # Apply rotation
        rotated_image = cv2.warpAffine(image, M, (width, height))
        
        return {
            "processed_image": encode_image_to_base64(rotated_image),
            "angle": angle,
            "scale": scale,
            "operation": "rotation"
        }
    except Exception as e:
        logger.error(f"Error in rotation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/flip")
async def flip_image(
    image_data: str = Form(...),
    flip_code: int = Form(1)  # 0=vertical, 1=horizontal, -1=both
):
    """Flip image"""
    try:
        image = decode_base64_image(image_data)
        
        # Apply flip
        flipped_image = cv2.flip(image, flip_code)
        
        flip_type = {0: "vertical", 1: "horizontal", -1: "both"}
        
        return {
            "processed_image": encode_image_to_base64(flipped_image),
            "flip_type": flip_type.get(flip_code, "unknown"),
            "operation": "flip"
        }
    except Exception as e:
        logger.error(f"Error in flip: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


#SCALING, RESIZING, CROPPING


@app.post("/api/resize")
async def resize_image(
    image_data: str = Form(...),
    scale_factor: float = Form(0.5),
    interpolation: str = Form("linear")
):
    """Resize image with different interpolation methods"""
    try:
        image = decode_base64_image(image_data)
        height, width = image.shape[:2]
        
        # Map interpolation methods
        interp_methods = {
            "nearest": cv2.INTER_NEAREST,
            "linear": cv2.INTER_LINEAR,
            "cubic": cv2.INTER_CUBIC,
            "lanczos": cv2.INTER_LANCZOS4
        }
        
        interp = interp_methods.get(interpolation, cv2.INTER_LINEAR)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        # Resize image
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=interp)
        
        return {
            "processed_image": encode_image_to_base64(resized_image),
            "original_size": [width, height],
            "new_size": [new_width, new_height],
            "scale_factor": scale_factor,
            "interpolation": interpolation,
            "operation": "resize"
        }
    except Exception as e:
        logger.error(f"Error in resize: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pyramid")
async def create_pyramid(
    image_data: str = Form(...),
    levels: int = Form(3)
):
    """Create image pyramid"""
    try:
        image = decode_base64_image(image_data)
        
        # Create Gaussian pyramid
        pyramid = [image]
        current = image.copy()
        
        for i in range(levels):
            current = cv2.pyrDown(current)
            pyramid.append(current)
        
        # Create a combined visualization
        height, width = image.shape[:2]
        result_image = np.zeros((height * 2, width * 2, 3), dtype=np.uint8)
        
        # Place original image
        result_image[:height, :width] = image
        
        # Place pyramid levels
        y_offset, x_offset = 0, width
        for level in pyramid[1:]:
            h, w = level.shape[:2]
            if y_offset + h <= height * 2 and x_offset + w <= width * 2:
                result_image[y_offset:y_offset+h, x_offset:x_offset+w] = level
                y_offset += h + 10
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "levels": levels,
            "operation": "image_pyramid"
        }
    except Exception as e:
        logger.error(f"Error creating pyramid: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crop")
async def crop_image(
    image_data: str = Form(...),
    x: int = Form(100),
    y: int = Form(100),
    width: int = Form(200),
    height: int = Form(200)
):
    """Crop image to specified region"""
    try:
        image = decode_base64_image(image_data)
        img_height, img_width = image.shape[:2]
        
        # Ensure crop coordinates are within image bounds
        x = max(0, min(x, img_width))
        y = max(0, min(y, img_height))
        width = min(width, img_width - x)
        height = min(height, img_height - y)
        
        # Crop image
        cropped_image = image[y:y+height, x:x+width]
        
        return {
            "processed_image": encode_image_to_base64(cropped_image),
            "crop_region": {"x": x, "y": y, "width": width, "height": height},
            "operation": "crop"
        }
    except Exception as e:
        logger.error(f"Error cropping image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ARITHMETIC AND BITWISE OPERATIONS


@app.post("/api/arithmetic")
async def arithmetic_operations(
    image_data: str = Form(...),
    operation: str = Form("add"),
    value: int = Form(50)
):
    """Perform arithmetic operations on image"""
    try:
        image = decode_base64_image(image_data)
        
        if operation == "add":
            result_image = cv2.add(image, np.ones(image.shape, dtype=np.uint8) * value)
        elif operation == "subtract":
            result_image = cv2.subtract(image, np.ones(image.shape, dtype=np.uint8) * value)
        elif operation == "multiply":
            result_image = cv2.multiply(image, value / 100.0)  # Scale factor
        elif operation == "divide":
            result_image = cv2.divide(image, value / 100.0)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
        
        return {
            "processed_image": encode_image_to_base64(result_image.astype(np.uint8)),
            "operation": f"arithmetic_{operation}",
            "value": value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bitwise")
async def bitwise_operations(
    image_data: str = Form(...),
    operation: str = Form("and"),
    mask_type: str = Form("circular")
):
    """Perform bitwise operations"""
    try:
        image = decode_base64_image(image_data)
        height, width = image.shape[:2]
        
        # Create mask
        if mask_type == "circular":
            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.circle(mask, (width//2, height//2), min(width, height)//4, 255, -1)
        elif mask_type == "rectangular":
            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.rectangle(mask, (width//4, height//4), (3*width//4, 3*height//4), 255, -1)
        else:
            mask = np.ones((height, width), dtype=np.uint8) * 255
        
        # Apply bitwise operation
        if operation == "and":
            result_image = cv2.bitwise_and(image, image, mask=mask)
        elif operation == "or":
            result_image = cv2.bitwise_or(image, cv2.merge([mask, mask, mask]))
        elif operation == "xor":
            result_image = cv2.bitwise_xor(image, cv2.merge([mask, mask, mask]))
        elif operation == "not":
            result_image = cv2.bitwise_not(image)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "mask_image": encode_image_to_base64(cv2.merge([mask, mask, mask])),
            "operation": f"bitwise_{operation}",
            "mask_type": mask_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#CONVOLUTIONS, BLURRING, SHARPENING


@app.post("/api/blur")
async def blur_image(
    image_data: str = Form(...),
    blur_type: str = Form("gaussian"),
    kernel_size: int = Form(15),
    sigma_x: float = Form(0),
    sigma_y: float = Form(0)
):
    """Apply various blur effects"""
    try:
        image = decode_base64_image(image_data)
        
        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        if blur_type == "gaussian":
            result_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma_x, sigma_y)
        elif blur_type == "motion":
            # Create motion blur kernel
            kernel = np.zeros((kernel_size, kernel_size))
            kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size)
            kernel = kernel / kernel_size
            result_image = cv2.filter2D(image, -1, kernel)
        elif blur_type == "median":
            result_image = cv2.medianBlur(image, kernel_size)
        elif blur_type == "bilateral":
            result_image = cv2.bilateralFilter(image, kernel_size, 80, 80)
        else:
            raise HTTPException(status_code=400, detail="Invalid blur type")
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "blur_type": blur_type,
            "kernel_size": kernel_size,
            "operation": "blur"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sharpen")
async def sharpen_image(
    image_data: str = Form(...),
    strength: float = Form(1.0)
):
    """Sharpen image using convolution"""
    try:
        image = decode_base64_image(image_data)
        
        # Define sharpening kernel
        kernel = np.array([[-1, -1, -1],
                          [-1, 9, -1],
                          [-1, -1, -1]]) * strength
        
        # Apply sharpening filter
        result_image = cv2.filter2D(image, -1, kernel)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "strength": strength,
            "operation": "sharpen"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/denoise")
async def denoise_image(
    image_data: str = Form(...),
    method: str = Form("nlmeans"),
    h: float = Form(10.0)
):
    """Remove noise from image"""
    try:
        image = decode_base64_image(image_data)
        
        if method == "nlmeans":
            result_image = cv2.fastNlMeansDenoisingColored(image, None, h, h, 7, 21)
        elif method == "bilateral":
            result_image = cv2.bilateralFilter(image, 9, 75, 75)
        elif method == "gaussian":
            result_image = cv2.GaussianBlur(image, (5, 5), 0)
        else:
            raise HTTPException(status_code=400, detail="Invalid denoising method")
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "method": method,
            "operation": "denoise"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# THRESHOLDING


@app.post("/api/threshold")
async def threshold_image(
    image_data: str = Form(...),
    threshold_value: int = Form(127),
    max_value: int = Form(255),
    threshold_type: str = Form("binary")
):
    """Apply binary thresholding"""
    try:
        image = decode_base64_image(image_data)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Map threshold types
        thresh_types = {
            "binary": cv2.THRESH_BINARY,
            "binary_inv": cv2.THRESH_BINARY_INV,
            "trunc": cv2.THRESH_TRUNC,
            "tozero": cv2.THRESH_TOZERO,
            "tozero_inv": cv2.THRESH_TOZERO_INV
        }
        
        thresh_type = thresh_types.get(threshold_type, cv2.THRESH_BINARY)
        
        # Apply threshold
        _, thresholded = cv2.threshold(gray_image, threshold_value, max_value, thresh_type)
        
        # Convert back to 3-channel for display
        result_image = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "threshold_value": threshold_value,
            "max_value": max_value,
            "threshold_type": threshold_type,
            "operation": "threshold"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/adaptive-threshold")
async def adaptive_threshold_image(
    image_data: str = Form(...),
    max_value: int = Form(255),
    adaptive_method: str = Form("mean"),
    threshold_type: str = Form("binary"),
    block_size: int = Form(11),
    c: int = Form(2)
):
    """Apply adaptive thresholding"""
    try:
        image = decode_base64_image(image_data)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Ensure block size is odd and >= 3
        if block_size % 2 == 0:
            block_size += 1
        block_size = max(3, block_size)
        
        # Map adaptive methods
        adaptive_methods = {
            "mean": cv2.ADAPTIVE_THRESH_MEAN_C,
            "gaussian": cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        }
        
        thresh_types = {
            "binary": cv2.THRESH_BINARY,
            "binary_inv": cv2.THRESH_BINARY_INV
        }
        
        adaptive_method_cv = adaptive_methods.get(adaptive_method, cv2.ADAPTIVE_THRESH_MEAN_C)
        thresh_type = thresh_types.get(threshold_type, cv2.THRESH_BINARY)
        
        # Apply adaptive threshold
        thresholded = cv2.adaptiveThreshold(
            gray_image, max_value, adaptive_method_cv, thresh_type, block_size, c
        )
        
        # Convert back to 3-channel for display
        result_image = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "adaptive_method": adaptive_method,
            "threshold_type": threshold_type,
            "block_size": block_size,
            "c": c,
            "operation": "adaptive_threshold"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# TOPIC 10: MORPHOLOGICAL OPERATIONS AND EDGE DETECTION
# =============================================================================

@app.post("/api/dilation")
async def dilate_image(
    image_data: str = Form(...),
    kernel_size: int = Form(5),
    iterations: int = Form(1)
):
    """Apply morphological dilation"""
    try:
        image = decode_base64_image(image_data)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create structuring element
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        
        # Apply dilation
        dilated = cv2.dilate(gray_image, kernel, iterations=iterations)
        
        # Convert back to 3-channel
        result_image = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "kernel_size": kernel_size,
            "iterations": iterations,
            "operation": "dilation"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/erosion")
async def erode_image(
    image_data: str = Form(...),
    kernel_size: int = Form(5),
    iterations: int = Form(1)
):
    """Apply morphological erosion"""
    try:
        image = decode_base64_image(image_data)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create structuring element
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        
        # Apply erosion
        eroded = cv2.erode(gray_image, kernel, iterations=iterations)
        
        # Convert back to 3-channel
        result_image = cv2.cvtColor(eroded, cv2.COLOR_GRAY2BGR)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "kernel_size": kernel_size,
            "iterations": iterations,
            "operation": "erosion"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/opening")
async def opening_image(
    image_data: str = Form(...),
    kernel_size: int = Form(5),
    iterations: int = Form(1)
):
    """Apply morphological opening (erosion followed by dilation)"""
    try:
        image = decode_base64_image(image_data)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create structuring element
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        
        # Apply opening
        opened = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, kernel, iterations=iterations)
        
        # Convert back to 3-channel
        result_image = cv2.cvtColor(opened, cv2.COLOR_GRAY2BGR)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "kernel_size": kernel_size,
            "iterations": iterations,
            "operation": "opening"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/closing")
async def closing_image(
    image_data: str = Form(...),
    kernel_size: int = Form(5),
    iterations: int = Form(1)
):
    """Apply morphological closing (dilation followed by erosion)"""
    try:
        image = decode_base64_image(image_data)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create structuring element
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        
        # Apply closing
        closed = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel, iterations=iterations)
        
        # Convert back to 3-channel
        result_image = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "kernel_size": kernel_size,
            "iterations": iterations,
            "operation": "closing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/edge-detection")
async def edge_detection(
    image_data: str = Form(...),
    low_threshold: int = Form(50),
    high_threshold: int = Form(150),
    aperture_size: int = Form(3),
    l2_gradient: bool = Form(False)
):
    """Apply Canny edge detection"""
    try:
        image = decode_base64_image(image_data)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
        
        # Apply Canny edge detection
        edges = cv2.Canny(blurred, low_threshold, high_threshold, 
                         apertureSize=aperture_size, L2gradient=l2_gradient)
        
        # Convert to 3-channel for display
        result_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        return {
            "processed_image": encode_image_to_base64(result_image),
            "low_threshold": low_threshold,
            "high_threshold": high_threshold,
            "aperture_size": aperture_size,
            "l2_gradient": l2_gradient,
            "operation": "edge_detection"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#
# BATCH PROCESSING


@app.post("/api/batch-process")
async def batch_process(
    files: List[UploadFile] = File(...),
    operation: str = Form(...),
    parameters: str = Form(default="{}")
):
    """Process multiple images with the same operation"""
    try:
        import json
        params = json.loads(parameters) if parameters else {}
        results = []
        
        for i, file in enumerate(files):
            try:
                # Read file content
                contents = await file.read()
                nparr = np.frombuffer(contents, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if image is None:
                    results.append({
                        "filename": file.filename,
                        "status": "error",
                        "error": "Invalid image file"
                    })
                    continue
                
                # Apply the operation based on type
                processed_image = None
                if operation == "grayscale":
                    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                elif operation == "blur":
                    blur_type = params.get("blur_type", "gaussian")
                    kernel_size = int(params.get("kernel_size", 15))
                    if blur_type == "gaussian":
                        processed_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
                    elif blur_type == "median":
                        processed_image = cv2.medianBlur(image, kernel_size)
                # Add more operations as needed
                
                if processed_image is not None:
                    results.append({
                        "filename": file.filename,
                        "status": "success",
                        "image": encode_image_to_base64(processed_image),
                        "operation": operation
                    })
                else:
                    results.append({
                        "filename": file.filename,
                        "status": "error",
                        "error": f"Operation {operation} not supported"
                    })
                    
            except Exception as e:
                logger.error(f"Error processing {file.filename}: {str(e)}")
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "results": results,
            "total_processed": len([r for r in results if r["status"] == "success"]),
            "total_failed": len([r for r in results if r["status"] == "error"]),
            "operation": operation
        }
        
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    logger.info("Starting ImageLab Processing Studio API...")
    uvicorn.run(
        "main:app",  # Use import string instead of app object
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=True
    )