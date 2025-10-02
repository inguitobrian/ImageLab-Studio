# ImageLab Studio

A professional image processing application built with **Vue.js 3**, **Electron**, and **FastAPI** backend. This application provides a comprehensive suite of OpenCV-based image processing operations with a modern, intuitive user interface.

![OpenCV Studio](https://img.shields.io/badge/OpenCV-Studio-blue)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red)
![Electron](https://img.shields.io/badge/Electron-27.0-purple)

## ✨ Features

### 🎯 Core Processing Operations
- **Getting Started**: Image loading, dimension analysis
- **Grayscaling**: Convert to grayscale, compare dimensions
- **Color Spaces**: RGB channel extraction, HSV conversion, color manipulation
- **Drawing & Shapes**: Add shapes, text, annotations
- **Transformations**: Rotation, translation, flipping
- **Scaling & Resizing**: Resize, crop, image pyramids
- **Arithmetic & Bitwise**: Mathematical operations on pixels
- **Filtering**: Gaussian blur, sharpening, denoising
- **Thresholding**: Binary and adaptive thresholding
- **Morphology**: Dilation, erosion, opening, closing
- **Edge Detection**: Canny edge detection

### 🚀 Advanced Features
- **Real-time Processing**: Live parameter adjustment with instant preview
- **Batch Processing**: Process multiple images simultaneously
- **Export Options**: PNG, JPG, PDF reports
- **Professional UI**: Modern glassmorphism design with dark theme
- **Cross-platform**: Windows, macOS, Linux support
- **Responsive Design**: Adaptive layout for different screen sizes

## 🛠️ Technology Stack

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Fast build tool and dev server
- **Electron** - Cross-platform desktop application framework
- **Modern CSS** - Glassmorphism design with advanced animations

### Backend
- **FastAPI** - Modern Python web framework
- **OpenCV** - Computer vision and image processing
- **NumPy** - Numerical computing
- **Pillow (PIL)** - Python Imaging Library

## 📦 Installation

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **pip** package manager

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/opencv-image-processing-studio.git
cd opencv-image-processing-studio
```

### 2. Install Frontend Dependencies
```bash
# Install npm packages
npm install

# Or using yarn
yarn install
```

### 3. Install Backend Dependencies
```bash
# Install Python packages
pip install fastapi
pip install uvicorn
pip install python-multipart
pip install opencv-python
pip install numpy
pip install pillow

# Or install from requirements.txt (if available)
pip install -r requirements.txt
```

## 🚀 Development Setup

### Start Backend Server
```bash
# Run the FastAPI backend
python main.py

# Backend will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Start Frontend Development Server
```bash
# In a new terminal, start Vue.js dev server
npm run dev

# Frontend will be available at http://localhost:3000
```

### Run Electron Application
```bash
# Start Electron in development mode
npm run electron-dev

# Or build and run
npm run build
npm run electron
```

## 📋 Available Scripts

### Frontend Scripts
```bash
npm run dev          # Start Vite development server
npm run build        # Build for production
npm run serve        # Preview production build
npm run electron     # Run Electron app
npm run electron-dev # Run Electron in development mode
npm run build-electron # Build Electron app for distribution
```

### Backend Scripts
```bash
python main.py       # Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000  # Alternative start method
```

## 🏗️ Project Structure

```
opencv-image-processing-studio/
├── backend/
│   ├── main.py        # Electron main process
│   ├── requirements.txt
├── electron/
│   ├── main.js
│   ├── preload.js
├── src/
│   ├── components/           # Vue.js components
│   │   ├── ImagePanel.vue
│   │   ├── ControlsPanel.vue
│   │   ├── BatchModal.vue
│   │   └── PDFModal.vue
│   ├── services/            # API services
│   │   └── imageProcessingService.js
│   ├── App.vue              # Main Vue component
│   ├── renderer.js          
│   └── style.css            # Global styles
├── main.js                  # VUE entry point         
├── main.py                  # FastAPI backend server
├── package.json             # Node.js dependencies
├── vite.config.js          # Vite configuration
├── index.html              # HTML entry point
└── README.md               # This file
```

## 🎮 Usage

### Basic Workflow
1. **Launch Application**: Start both backend and frontend servers
2. **Load Image**: Click "Load Image" or use Ctrl+O
3. **Select Operation**: Choose from the sidebar operations
4. **Adjust Parameters**: Use the controls panel for real-time adjustments
5. **Export Results**: Save processed images in various formats

### Keyboard Shortcuts
- `Ctrl+O` - Open image
- `Ctrl+S` - Save processed image
- `Ctrl+B` - Open batch processing
- `Ctrl+P` - Export PDF report

### API Endpoints
The backend provides RESTful API endpoints:
- `GET /health` - Health check
- `POST /api/grayscale` - Convert to grayscale
- `POST /api/blur` - Apply blur effects
- `POST /api/rotate` - Rotate image
- `POST /api/threshold` - Apply thresholding
- `POST /api/edge-detection` - Canny edge detection
- And many more...

Full API documentation available at `http://localhost:8000/docs`

## 🔧 Configuration

### Backend Configuration
Modify `main.py` to change:
- Server host and port
- CORS settings
- Image processing parameters
- Logging levels

### Frontend Configuration
Modify `vite.config.js` to change:
- Development server settings
- Build options
- Asset handling

### Electron Configuration
Modify `main.js` to change:
- Window properties
- Menu structure
- Security settings

## 📸 Screenshots

### Main Interface
The application features a modern, professional interface with:
- Sidebar with categorized operations
- Dual-panel image display (original vs processed)
- Dynamic controls panel
- Real-time processing feedback

### Batch Processing
- Drag-and-drop file support
- Progress tracking
- Bulk operations on multiple images
- Download images as zip file

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenCV](https://opencv.org/) - Computer vision library
- [Vue.js](https://vuejs.org/) - Progressive JavaScript framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Electron](https://www.electronjs.org/) - Cross-platform desktop apps


