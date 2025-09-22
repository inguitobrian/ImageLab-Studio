import axios from "axios";

const BACKEND_URL = "http://localhost:8000";

class ImageProcessingService {
  constructor() {
    this.api = axios.create({
      baseURL: BACKEND_URL,
      timeout: 60000, // Increase timeout to 60 seconds
      headers: {
        "Content-Type": "application/json",
      },
      maxContentLength: 50 * 1024 * 1024, // 50MB
      maxBodyLength: 50 * 1024 * 1024, // 50MB
    });
  }

  // Add image compression method
  compressImage(base64String, maxSizeKB = 800) {
    return new Promise((resolve) => {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      const img = new Image();

      img.onload = () => {
        // Calculate new dimensions to reduce file size
        let { width, height } = img;
        const maxDimension = 1920; // Max width or height

        if (width > maxDimension || height > maxDimension) {
          if (width > height) {
            height = (height * maxDimension) / width;
            width = maxDimension;
          } else {
            width = (width * maxDimension) / height;
            height = maxDimension;
          }
        }

        canvas.width = width;
        canvas.height = height;

        // Draw and compress
        ctx.drawImage(img, 0, 0, width, height);

        // Start with high quality and reduce if needed
        let quality = 0.9;
        let compressedData = canvas.toDataURL("image/jpeg", quality);

        // Reduce quality until size is acceptable
        while (
          this.getBase64Size(compressedData) > maxSizeKB * 1024 &&
          quality > 0.1
        ) {
          quality -= 0.1;
          compressedData = canvas.toDataURL("image/jpeg", quality);
        }

        resolve(compressedData.split(",")[1]); // Return base64 without prefix
      };

      img.src = `data:image/jpeg;base64,${base64String}`;
    });
  }

  getBase64Size(base64String) {
    const base64 = base64String.split(",")[1] || base64String;
    return Math.ceil(base64.length * 0.75); // Approximate size in bytes
  }

  async checkHealth() {
    try {
      const response = await this.api.get("/health");
      return response.data;
    } catch (error) {
      throw new Error("Backend connection failed");
    }
  }

  async processImage(operation, imageData, parameters = {}) {
    try {
      // Compress image if it's too large
      const imageSize = this.getBase64Size(imageData);
      let processedImageData = imageData;

      if (imageSize > 800 * 1024) {
        // If larger than 800KB
        console.log(`Compressing image (${(imageSize / 1024).toFixed(1)}KB)`);
        processedImageData = await this.compressImage(imageData, 800);
        console.log(
          `Compressed to ${(
            this.getBase64Size(processedImageData) / 1024
          ).toFixed(1)}KB`
        );
      }

      const formData = new FormData();
      formData.append("image_data", processedImageData);

      // Add operation-specific parameters
      Object.entries(parameters).forEach(([key, value]) => {
        formData.append(key, value);
      });

      const response = await this.api.post(`/api/${operation}`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        maxContentLength: 50 * 1024 * 1024, // 50MB
        maxBodyLength: 50 * 1024 * 1024, // 50MB
      });

      return response.data;
    } catch (error) {
      console.error(`Error processing ${operation}:`, error);
      throw new Error(
        error.response?.data?.detail || `Processing failed: ${error.message}`
      );
    }
  }

  async loadImage(file) {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await this.api.post("/api/load-image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      return response.data;
    } catch (error) {
      console.error("Error loading image:", error);
      throw new Error(
        error.response?.data?.detail || `Image loading failed: ${error.message}`
      );
    }
  }

  async getDimensions(imageData) {
    try {
      const formData = new FormData();
      formData.append("image_data", imageData);

      const response = await this.api.post("/api/dimensions", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      return response.data;
    } catch (error) {
      console.error("Error getting dimensions:", error);
      throw new Error(
        error.response?.data?.detail ||
          `Dimension check failed: ${error.message}`
      );
    }
  }

  async batchProcess(files, operation, parameters = {}) {
    try {
      console.log(
        `Starting batch processing: ${files.length} files with ${operation}`
      );
      console.log("Parameters:", parameters);

      // Validate operation
      if (!operation) {
        throw new Error("No operation specified for batch processing");
      }

      const formData = new FormData();

      // Process each file individually to ensure proper compression
      for (let i = 0; i < files.length; i++) {
        const file = files[i];

        // Convert file to base64 and compress if needed
        const base64Data = await this.fileToBase64(file);
        const imageSize = this.getBase64Size(base64Data);

        let processedImageData = base64Data;
        if (imageSize > 800 * 1024) {
          // If larger than 800KB
          console.log(
            `Compressing file ${i + 1} (${(imageSize / 1024).toFixed(1)}KB)`
          );
          processedImageData = await this.compressImage(base64Data, 800);
        }

        // Create a new File object with compressed data
        const compressedBlob = this.base64ToBlob(processedImageData, file.type);
        const compressedFile = new File([compressedBlob], file.name, {
          type: file.type,
        });

        formData.append("files", compressedFile);
      }

      // Add operation (ensure it's properly set)
      formData.append("operation", operation);

      // Add parameters as individual form fields for better backend parsing
      Object.entries(parameters).forEach(([key, value]) => {
        formData.append(`param_${key}`, String(value));
      });

      // Also include parameters as JSON for backward compatibility
      formData.append("parameters", JSON.stringify(parameters));

      console.log("Sending batch request with operation:", operation);
      console.log("Parameters being sent:", parameters);

      const response = await this.api.post("/api/batch-process", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 300000, // 5 minutes timeout for batch processing
        maxContentLength: 100 * 1024 * 1024, // 100MB
        maxBodyLength: 100 * 1024 * 1024, // 100MB
      });

      console.log("Batch processing completed:", response.data);
      return response.data;
    } catch (error) {
      console.error("Batch processing error:", error);
      throw new Error(
        error.response?.data?.detail ||
          `Batch processing failed: ${error.message}`
      );
    }
  }

  // Helper method to convert file to base64
  fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = reader.result.split(",")[1];
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  // Helper method to convert base64 back to blob
  base64ToBlob(base64Data, mimeType) {
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
  }

  async getAvailableOperations() {
    try {
      const response = await this.api.get("/api/operations");
      return response.data;
    } catch (error) {
      console.error("Error getting operations:", error);
      throw new Error("Failed to get available operations");
    }
  }

  async getOperationParameters(operation) {
    try {
      const response = await this.api.get(`/api/parameters/${operation}`);
      return response.data;
    } catch (error) {
      console.error(`Error getting parameters for ${operation}:`, error);
      throw new Error(`Failed to get parameters for ${operation}`);
    }
  }

  // Specialized processing methods
  async convertToGrayscale(imageData) {
    return this.processImage("grayscale", imageData);
  }

  async extractRGBChannels(imageData) {
    return this.processImage("rgb-channels", imageData);
  }

  async convertToHSV(imageData) {
    return this.processImage("hsv-convert", imageData);
  }

  async rotateImage(imageData, angle = 45, scale = 1.0) {
    return this.processImage("rotate", imageData, { angle, scale });
  }

  async blurImage(imageData, blurType = "gaussian", kernelSize = 15) {
    return this.processImage("blur", imageData, {
      blur_type: blurType,
      kernel_size: kernelSize,
    });
  }

  async thresholdImage(
    imageData,
    thresholdValue = 127,
    thresholdType = "binary"
  ) {
    return this.processImage("threshold", imageData, {
      threshold_value: thresholdValue,
      threshold_type: thresholdType,
      max_value: 255,
    });
  }

  async resizeImage(imageData, scaleFactor = 0.5, interpolation = "linear") {
    return this.processImage("resize", imageData, {
      scale_factor: scaleFactor,
      interpolation,
    });
  }

  async detectEdges(imageData, lowThreshold = 50, highThreshold = 150) {
    return this.processImage("edge-detection", imageData, {
      low_threshold: lowThreshold,
      high_threshold: highThreshold,
    });
  }

  async cropImage(imageData, x = 100, y = 100, width = 200, height = 200) {
    return this.processImage("crop", imageData, { x, y, width, height });
  }

  async translateImage(imageData, tx = 50, ty = 50) {
    return this.processImage("translate", imageData, { tx, ty });
  }

  async flipImage(imageData, flipCode = 1) {
    return this.processImage("flip", imageData, { flip_code: flipCode });
  }

  async drawShapes(imageData) {
    return this.processImage("draw-shapes", imageData);
  }

  async addText(
    imageData,
    text = "OpenCV Text",
    fontScale = 1.0,
    colorR = 255,
    colorG = 255,
    colorB = 255
  ) {
    return this.processImage("add-text", imageData, {
      text,
      font_scale: fontScale,
      color_r: colorR,
      color_g: colorG,
      color_b: colorB,
    });
  }

  async performArithmetic(imageData, operation = "add", value = 50) {
    return this.processImage("arithmetic", imageData, { operation, value });
  }

  async performBitwise(imageData, operation = "and", maskType = "circular") {
    return this.processImage("bitwise", imageData, {
      operation,
      mask_type: maskType,
    });
  }

  async sharpenImage(imageData, strength = 1.0) {
    return this.processImage("sharpen", imageData, { strength });
  }

  async denoiseImage(imageData, method = "nlmeans", h = 10.0) {
    return this.processImage("denoise", imageData, { method, h });
  }

  async adaptiveThreshold(
    imageData,
    maxValue = 255,
    adaptiveMethod = "mean",
    thresholdType = "binary",
    blockSize = 11,
    c = 2
  ) {
    return this.processImage("adaptive-threshold", imageData, {
      max_value: maxValue,
      adaptive_method: adaptiveMethod,
      threshold_type: thresholdType,
      block_size: blockSize,
      c,
    });
  }

  async dilateImage(imageData, kernelSize = 5, iterations = 1) {
    return this.processImage("dilation", imageData, {
      kernel_size: kernelSize,
      iterations,
    });
  }

  async erodeImage(imageData, kernelSize = 5, iterations = 1) {
    return this.processImage("erosion", imageData, {
      kernel_size: kernelSize,
      iterations,
    });
  }

  async openingImage(imageData, kernelSize = 5, iterations = 1) {
    return this.processImage("opening", imageData, {
      kernel_size: kernelSize,
      iterations,
    });
  }

  async closingImage(imageData, kernelSize = 5, iterations = 1) {
    return this.processImage("closing", imageData, {
      kernel_size: kernelSize,
      iterations,
    });
  }

  async createPyramid(imageData, levels = 3) {
    return this.processImage("pyramid", imageData, { levels });
  }

  async manipulateColor(
    imageData,
    hueShift = 0,
    saturationFactor = 1.0,
    valueFactor = 1.0
  ) {
    return this.processImage("color-manipulation", imageData, {
      hue_shift: hueShift,
      saturation_factor: saturationFactor,
      value_factor: valueFactor,
    });
  }

  async compareDimensions(imageData) {
    return this.processImage("compare-dimensions", imageData);
  }
}

export const imageProcessingService = new ImageProcessingService();
export default ImageProcessingService;
