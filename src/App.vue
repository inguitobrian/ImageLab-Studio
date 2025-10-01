<template>
  <div class="app-container">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </div>
          <div>
            <h1>ImageLab Studio</h1>
            <p>CSC-126 Topic 1 to 10 Image Processing</p>
          </div>
        </div>
      </div>

      <div class="operations-section">
        <!-- Getting Started -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">🚀</span>
            Getting Started
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'dimensions' }"
            @click="selectOperation('dimensions', $event)"
          >
            <span class="btn-icon">📏</span>
            Show Dimensions
            <span class="btn-arrow">→</span>
          </button>
        </div>

        <!-- Grayscaling -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">⚫</span>
            Grayscaling
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'grayscale' }"
            @click="selectOperation('grayscale', $event)"
          >
            <span class="btn-icon">🎨</span>
            Convert to Grayscale
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'compare-dimensions' }"
            @click="selectOperation('compare-dimensions', $event)"
          >
            <span class="btn-icon">📊</span>
            Compare Dimensions
            <span class="btn-arrow">→</span>
          </button>
        </div>

        <!-- Color Spaces -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">🌈</span>
            Color Spaces
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'rgb-channels' }"
            @click="selectOperation('rgb-channels', $event)"
          >
            <span class="btn-icon">🔴</span>
            RGB Channels
            <span class="btn-arrow">→</span>
          </button>

          <div
            v-if="currentOperation === 'rgb-channels'"
            class="rgb-channel-selection"
          >
            <div class="channel-selection-title">Select Channel:</div>
            <div class="channel-buttons">
              <button class="channel-btn red-btn" @click="extractRedChannel">
                <span class="channel-icon">🔴</span>
                <span class="channel-name">Red Channel</span>
              </button>
              <button
                class="channel-btn green-btn"
                @click="extractGreenChannel"
              >
                <span class="channel-icon">🟢</span>
                <span class="channel-name">Green Channel</span>
              </button>
              <button class="channel-btn blue-btn" @click="extractBlueChannel">
                <span class="channel-icon">🔵</span>
                <span class="channel-name">Blue Channel</span>
              </button>
            </div>
          </div>

          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'hsv-convert' }"
            @click="selectOperation('hsv-convert', $event)"
          >
            <span class="btn-icon">🎯</span>
            HSV Conversion
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'color-manipulation' }"
            @click="selectOperation('color-manipulation', $event)"
          >
            <span class="btn-icon">🎪</span>
            Color Manipulation
            <span class="btn-arrow">→</span>
          </button>
        </div>

        <!-- Drawing & Shapes -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">✏️</span>
            Drawing & Shapes
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'draw-shapes' }"
            @click="selectOperation('draw-shapes', $event)"
          >
            <span class="btn-icon">🔷</span>
            Interactive Drawing
            <span class="btn-arrow">→</span>
          </button>

          <!-- Shape Selection Buttons (show when Interactive Drawing is active) -->
          <div
            v-if="currentOperation === 'draw-shapes'"
            class="shape-selection"
          >
            <div class="shape-selection-title">Choose Shape:</div>
            <div class="shape-buttons">
              <button
                v-for="tool in availableTools"
                :key="tool.type"
                class="shape-btn"
                :class="{ active: currentDrawingTool === tool.type }"
                @click="selectDrawingTool(tool.type)"
              >
                <span class="shape-icon">{{ tool.icon }}</span>
                <span class="shape-name">{{ tool.name }}</span>
              </button>
            </div>

            <!-- Quick Drawing Controls -->
            <div class="quick-controls">
              <div class="control-row">
                <label>Color:</label>
                <input
                  type="color"
                  :value="rgbToHex(drawingColor)"
                  @input="updateColor($event.target.value)"
                  class="mini-color-picker"
                />
              </div>
              <div class="control-row">
                <label>Thickness:</label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  v-model="drawingThickness"
                  class="mini-slider"
                />
                <span class="value-display">{{ drawingThickness }}</span>
              </div>
              <div
                class="control-row"
                v-if="
                  ['rectangle', 'circle', 'polygon'].includes(
                    currentDrawingTool
                  )
                "
              >
                <label>
                  <input
                    type="checkbox"
                    v-model="drawingFilled"
                    class="mini-checkbox"
                  />
                  Fill Shape
                </label>
              </div>
            </div>

            <!-- Drawing Action Buttons -->
            <div class="drawing-actions">
              <button class="action-btn clear-btn" @click="clearDrawing">
                🗑️ Clear
              </button>
              <button
                class="action-btn apply-btn"
                @click="applyAllShapes"
                :disabled="currentShapes.length === 0"
              >
                ✅ Apply
              </button>
              <button class="action-btn finish-btn" @click="finishDrawing">
                🏁 Done
              </button>
            </div>
          </div>

          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'draw-freehand' }"
            @click="selectOperation('draw-freehand', $event)"
          >
            <span class="btn-icon">✏️</span>
            Freehand Drawing
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'add-text' }"
            @click="selectOperation('add-text', $event)"
          >
            <span class="btn-icon">📝</span>
            Custom Text
            <span class="btn-arrow">→</span>
          </button>
        </div>

        <!-- Transformations -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">🔄</span>
            Transformations
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'translate' }"
            @click="selectOperation('translate', $event)"
          >
            <span class="btn-icon">📍</span>
            Translation
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'rotate' }"
            @click="selectOperation('rotate', $event)"
          >
            <span class="btn-icon">🔄</span>
            Rotation
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'flip' }"
            @click="selectOperation('flip', $event)"
          >
            <span class="btn-icon">🔀</span>
            Flip Image
            <span class="btn-arrow">→</span>
          </button>
        </div>

        <!-- Scaling & Resizing -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">📏</span>
            Scaling & Resizing
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'resize' }"
            @click="selectOperation('resize', $event)"
          >
            <span class="btn-icon">📐</span>
            Resize Image
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'pyramid' }"
            @click="selectOperation('pyramid', $event)"
          >
            <span class="btn-icon">🏔️</span>
            Image Pyramid
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'crop' }"
            @click="selectOperation('crop', $event)"
          >
            <span class="btn-icon">✂️</span>
            Crop Image
            <span class="btn-arrow">→</span>
          </button>
        </div>

        <!-- Arithmetic & Bitwise -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">🧮</span>
            Arithmetic & Bitwise
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'arithmetic' }"
            @click="selectOperation('arithmetic', $event)"
          >
            <span class="btn-icon">➕</span>
            Arithmetic Ops
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'bitwise' }"
            @click="selectOperation('bitwise', $event)"
          >
            <span class="btn-icon">⚡</span>
            Bitwise Ops
            <span class="btn-arrow">→</span>
          </button>
        </div>

        <!-- Filtering -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">✨</span>
            Filtering & Enhancement
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'blur' }"
            @click="selectOperation('blur', $event)"
          >
            <span class="btn-icon">🌀</span>
            Blur Effects
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'sharpen' }"
            @click="selectOperation('sharpen', $event)"
          >
            <span class="btn-icon">🔪</span>
            Sharpen Image
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'denoise' }"
            @click="selectOperation('denoise', $event)"
          >
            <span class="btn-icon">🧹</span>
            Denoise
            <span class="btn-arrow">→</span>
          </button>
        </div>

        <!-- Thresholding -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">⚖️</span>
            Thresholding
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'threshold' }"
            @click="selectOperation('threshold', $event)"
          >
            <span class="btn-icon">⚫</span>
            Binary Threshold
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'adaptive-threshold' }"
            @click="selectOperation('adaptive-threshold', $event)"
          >
            <span class="btn-icon">🎛️</span>
            Adaptive Threshold
            <span class="btn-arrow">→</span>
          </button>
        </div>

        <!-- Morphology & Edge Detection -->
        <div class="operation-group">
          <div class="section-title">
            <span class="section-icon">🔍</span>
            Morphology & Edges
          </div>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'dilation' }"
            @click="selectOperation('dilation', $event)"
          >
            <span class="btn-icon">📈</span>
            Dilation
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'erosion' }"
            @click="selectOperation('erosion', $event)"
          >
            <span class="btn-icon">📉</span>
            Erosion
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'opening' }"
            @click="selectOperation('opening', $event)"
          >
            <span class="btn-icon">🌅</span>
            Opening
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'closing' }"
            @click="selectOperation('closing', $event)"
          >
            <span class="btn-icon">🌄</span>
            Closing
            <span class="btn-arrow">→</span>
          </button>
          <button
            class="operation-btn"
            :class="{ active: currentOperation === 'edge-detection' }"
            @click="selectOperation('edge-detection', $event)"
          >
            <span class="btn-icon">📍</span>
            Canny Edge Detection
            <span class="btn-arrow">→</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Header -->
      <div class="header">
        <div class="header-left">
          <div class="breadcrumb">
            <span class="breadcrumb-item">Dashboard</span>
            <span class="breadcrumb-separator">›</span>
            <span class="breadcrumb-item active">Image Processing</span>
          </div>
        </div>
      </div>

      <!-- Toolbar -->
      <div class="toolbar">
        <div class="toolbar-left">
          <div class="file-input-wrapper">
            <input
              type="file"
              ref="imageInput"
              class="file-input"
              accept="image/*"
              @change="handleImageLoad"
            />
            <button class="btn btn-primary" @click="$refs.imageInput.click()">
              <span class="btn-icon">📁</span>
              Load Image
            </button>
          </div>
          <button class="btn btn-secondary" @click="openBatchModal">
            <span class="btn-icon">📚</span>
            Batch Process
          </button>
        </div>
        <div class="toolbar-right">
          <div class="export-dropdown">
            <button class="btn btn-success" @click="toggleExportDropdown">
              <span class="btn-icon">💾</span>
              Export Results
              <span class="dropdown-arrow">▼</span>
            </button>
            <div
              class="export-dropdown-menu"
              :class="{ active: exportDropdownActive }"
            >
              <button class="export-option" @click="exportAs('png')">
                <span class="export-icon">🖼️</span>
                PNG Image
              </button>
              <button class="export-option" @click="exportAs('jpg')">
                <span class="export-icon">📸</span>
                JPG Image
              </button>
              <button class="export-option" @click="exportAsPDF">
                <span class="export-icon">📄</span>
                PDF Report
              </button>
              <button class="export-option" @click="exportAll">
                <span class="export-icon">📦</span>
                Export All
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Image Workspace -->
      <div class="workspace">
        <div class="image-container">
          <ImagePanel
            title="Original Image"
            :image="currentImage"
            :info="originalInfo"
            @load-image="$refs.imageInput.click()"
          />

          <ImagePanel
            title="Processed Image"
            :image="processedImage"
            :info="processedInfo"
            :is-processed="true"
          />
        </div>

        <!-- Dynamic Controls Panel -->
        <ControlsPanel
          v-if="showControls"
          :operation="currentOperation"
          @close="closeControls"
          @update="updateParameters"
        />
      </div>
    </div>

    <!-- Status Bar Modal -->
    <div
      v-if="showStatusModal"
      class="status-modal-overlay"
      @click="closeStatusModal"
    >
      <div class="status-modal" @click.stop>
        <div class="status-modal-header">
          <h3>Application Status</h3>
          <button class="close-btn" @click="closeStatusModal">×</button>
        </div>
        <div class="status-modal-content">
          <div class="status-item">
            <label>Current Status:</label>
            <span>{{ statusText }}</span>
          </div>
          <div class="status-item" v-if="progress > 0">
            <label>Progress:</label>
            <div class="modal-progress-container">
              <div class="modal-progress-bar">
                <div
                  class="modal-progress-fill"
                  :style="{ width: progress + '%' }"
                ></div>
              </div>
              <span class="modal-progress-text">{{ progress }}%</span>
            </div>
          </div>
          <div class="status-item">
            <label>Images:</label>
            <span>{{ imageCount }}</span>
          </div>
          <div class="status-item">
            <label>Backend:</label>
            <span
              :class="{
                'status-online': backendConnected,
                'status-offline': !backendConnected,
              }"
            >
              {{ backendStatus }}
            </span>
          </div>
          <div class="status-item" v-if="currentOperation">
            <label>Current Operation:</label>
            <span>{{ currentOperation.replace(/-/g, " ") }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Status Bar Toggle Button (minimal) -->
    <div class="status-toggle">
      <button
        class="status-toggle-btn"
        @click="toggleStatusModal"
        :class="{ 'has-progress': progress > 0 }"
      >
        <span class="status-icon">📊</span>
        <span class="status-brief">{{
          statusText.length > 20
            ? statusText.substring(0, 20) + "..."
            : statusText
        }}</span>
        <div
          v-if="progress > 0"
          class="mini-progress"
          :style="{ width: progress + '%' }"
        ></div>
      </button>
    </div>

    <!-- Batch Processing Modal -->
    <BatchModal
      v-if="batchModalActive"
      :files="batchFiles"
      @close="closeBatchModal"
      @add-files="handleBatchFiles"
      @remove-file="removeBatchFile"
      @start-processing="startBatchProcessing"
    />

    <!-- PDF Report Modal -->
    <PDFModal
      v-if="pdfModalActive"
      @close="closePDFModal"
      @generate="generatePDFReport"
    />
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from "vue";
import ImagePanel from "./components/ImagePanel.vue";
import ControlsPanel from "./components/ControlsPanel.vue";
import BatchModal from "./components/BatchModal.vue";
import PDFModal from "./components/PdfModal.vue";
import { imageProcessingService } from "./services/ImageProcessingService";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

export default {
  name: "App",
  components: {
    ImagePanel,
    ControlsPanel,
    BatchModal,
    PDFModal,
  },
  setup() {
    // Reactive data
    const showStatusModal = ref(false);
    const currentImage = ref(null);
    const toggleStatusModal = () => {
      showStatusModal.value = !showStatusModal.value;
    };
    const closeStatusModal = () => {
      showStatusModal.value = false;
    };
    const processedImage = ref(null);
    const currentOperation = ref(null);
    const showControls = ref(false);
    const backendConnected = ref(false);
    const backendStatus = ref("Disconnected");
    const statusText = ref("Application ready");
    const progress = ref(0);
    const imageCount = ref("No images loaded");
    const exportDropdownActive = ref(false);
    const batchModalActive = ref(false);
    const pdfModalActive = ref(false);

    const availableTools = ref([
      { type: "rectangle", name: "Rectangle", icon: "▭" },
      { type: "circle", name: "Circle", icon: "●" },
      { type: "line", name: "Line", icon: "─" },
      { type: "arrow", name: "Arrow", icon: "→" },
      { type: "polygon", name: "Polygon", icon: "⬟" },
    ]);

    // New drawing-related data
    const drawingMode = ref(null);
    const currentShapes = ref([]);
    const freehandPoints = ref([]);
    const textElements = ref([]);
    const isDrawing = ref(false);
    const currentDrawingTool = ref("rectangle");
    const drawingColor = ref([255, 0, 0]); // Default red
    const drawingThickness = ref(2);
    const drawingFilled = ref(false);

    // Drawing state for shapes
    const drawingState = reactive({
      startX: 0,
      startY: 0,
      currentX: 0,
      currentY: 0,
      isDrawing: false,
      previewShape: null,
    });

    // Example usage in frontend
    const polygonShape = {
      type: "polygon",
      polygon_type: "pentagon", // or 'triangle', 'hexagon', 'star', etc.
      center_x: 200,
      center_y: 150,
      size: 80,
      color: [255, 0, 0],
      thickness: 3,
      filled: false,
    };

    const selectDrawingTool = (toolType) => {
      currentDrawingTool.value = toolType;
      statusText.value = `Selected ${toolType} tool - Click on image to draw`;
    };

    const rgbToHex = (rgb) => {
      return (
        "#" +
        ((1 << 24) + (rgb[0] << 16) + (rgb[1] << 8) + rgb[2])
          .toString(16)
          .slice(1)
      );
    };

    const updateColor = (hexColor) => {
      const r = parseInt(hexColor.slice(1, 3), 16);
      const g = parseInt(hexColor.slice(3, 5), 16);
      const b = parseInt(hexColor.slice(5, 7), 16);
      drawingColor.value = [r, g, b];
    };

    const originalInfo = reactive({
      status: "No image loaded",
    });

    const processedInfo = reactive({
      status: "No processing applied",
    });

    const batchFiles = ref([]);
    const operationParameters = reactive({});

    // Methods
    const checkBackendConnection = async () => {
      try {
        const response = await imageProcessingService.checkHealth();
        if (response.status === "healthy") {
          backendConnected.value = true;
          backendStatus.value = `Connected (OpenCV ${response.opencv_version})`;
        }
      } catch (error) {
        backendConnected.value = false;
        backendStatus.value = "Disconnected";
        console.warn("Backend connection failed:", error);
      }
    };

    const handleImageLoad = (event) => {
      const file = event.target.files[0];
      if (file) {
        loadImage(file);
        imageCount.value = "1 image loaded";
      }
    };

    const loadImage = (file) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        currentImage.value = e.target.result;
        updateImageInfo(file);
        statusText.value = `Loaded: ${file.name}`;

        // Reset processed image
        processedImage.value = null;
        processedInfo.status = "No processing applied";

        // Reset active operation
        currentOperation.value = null;
        showControls.value = false;
      };
      reader.readAsDataURL(file);
    };

    const updateImageInfo = (file) => {
      const img = new Image();
      img.onload = () => {
        originalInfo.filename = file.name;
        originalInfo.size = `${(file.size / 1024).toFixed(1)} KB`;
        originalInfo.dimensions = `${img.width} × ${img.height} pixels`;
        originalInfo.type = file.type;
        originalInfo.status = "Image loaded";
      };
      img.src = URL.createObjectURL(file);
    };

    // (Removed duplicate selectOperation to fix redeclaration error)

    const processImage = async (operation) => {
      if (!currentImage.value) return;

      statusText.value = `Processing: ${operation}...`;
      progress.value = 30;

      try {
        const base64Data = currentImage.value.split(",")[1];
        const params = getOperationParameters(operation);

        const result = await imageProcessingService.processImage(
          operation,
          base64Data,
          params
        );

        if (result.processed_image) {
          processedImage.value = `data:image/png;base64,${result.processed_image}`;
        } else if (
          result.red_channel &&
          result.green_channel &&
          result.blue_channel
        ) {
          // Handle RGB channel extraction with user selection
          const channelType = params.channel_type || "red"; // default to red

          switch (channelType) {
            case "red":
              processedImage.value = `data:image/png;base64,${result.red_channel}`;
              processedInfo.operation = "Red Channel Extraction";
              break;
            case "green":
              processedImage.value = `data:image/png;base64,${result.green_channel}`;
              processedInfo.operation = "Green Channel Extraction";
              break;
            case "blue":
              processedImage.value = `data:image/png;base64,${result.blue_channel}`;
              processedInfo.operation = "Blue Channel Extraction";
              break;
            case "combined":
              // Show a composite view or just default to red
              processedImage.value = `data:image/png;base64,${result.red_channel}`;
              processedInfo.operation = "RGB Channels (Red View)";
              break;
          }
        } else if (result.hsv_image) {
          processedImage.value = `data:image/png;base64,${result.hsv_image}`;
        }

        processedInfo.status = "Complete";
        processedInfo.backend = "FastAPI + OpenCV";

        progress.value = 100;
        showMessage("Processing complete!", "success");

        setTimeout(() => {
          statusText.value = "Ready";
          progress.value = 0;
        }, 1000);
      } catch (error) {
        console.error("Processing error:", error);
        statusText.value = `Error: ${error.message}`;
        progress.value = 0;
        showMessage(`Error: ${error.message}`, "error");

        processedInfo.status = "Processing failed";
      }
    };

    // Add RGB channel selection functionality
    const selectRGBChannel = (channelType) => {
      if (!currentImage.value) {
        showMessage("Please load an image first!", "error");
        return;
      }

      // Update the operation parameters
      operationParameters["rgb-channels"] = { channel_type: channelType };

      // Process the image with the selected channel
      processImage("rgb-channels");

      statusText.value = `Extracting ${channelType} channel...`;
    };

    // Quick RGB channel buttons
    const extractRedChannel = () => selectRGBChannel("red");
    const extractGreenChannel = () => selectRGBChannel("green");
    const extractBlueChannel = () => selectRGBChannel("blue");

    const getOperationParameters = (operation) => {
      return operationParameters[operation] || {};
    };

    // (Removed duplicate updateParameters to fix redeclaration error)

    const selectOperation = async (operation, event) => {
      if (!currentImage.value) {
        showMessage("Please load an image first!", "error");
        return;
      }

      currentOperation.value = operation;
      showControls.value = true;

      // Handle drawing operations differently
      if (operation === "draw-shapes") {
        initializeDrawingMode("shapes");
      } else if (operation === "draw-freehand") {
        initializeDrawingMode("freehand");
      } else if (operation === "add-text") {
        initializeDrawingMode("text");
      } else {
        await processImage(operation);
      }
    };

    const initializeDrawingMode = (mode) => {
      drawingMode.value = mode;
      currentShapes.value = [];
      freehandPoints.value = [];
      textElements.value = [];

      statusText.value = `${mode} drawing mode active - Click on image to draw`;

      // Setup canvas overlay for drawing
      nextTick(() => {
        setupDrawingCanvas();
      });
    };

    const setupDrawingCanvas = () => {
      const imageContainer = document.querySelector(".image-container");
      if (!imageContainer) return;

      // Remove existing canvas if any
      const existingCanvas = document.getElementById("drawing-canvas");
      if (existingCanvas) {
        existingCanvas.remove();
      }

      // Create new canvas overlay
      const canvas = document.createElement("canvas");
      canvas.id = "drawing-canvas";
      canvas.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        cursor: crosshair;
        z-index: 10;
        pointer-events: auto;
      `;

      // Set canvas size to match image
      const img = imageContainer.querySelector("img");
      if (img) {
        canvas.width = img.clientWidth;
        canvas.height = img.clientHeight;
        canvas.style.width = img.clientWidth + "px";
        canvas.style.height = img.clientHeight + "px";
      }

      imageContainer.style.position = "relative";
      imageContainer.appendChild(canvas);

      // Add drawing event listeners
      setupDrawingEvents(canvas);
    };

    const setupDrawingEvents = (canvas) => {
      const ctx = canvas.getContext("2d");

      canvas.addEventListener("mousedown", handleDrawStart);
      canvas.addEventListener("mousemove", handleDrawMove);
      canvas.addEventListener("mouseup", handleDrawEnd);
      canvas.addEventListener("click", handleCanvasClick);

      // Touch events for mobile
      canvas.addEventListener("touchstart", handleTouchStart);
      canvas.addEventListener("touchmove", handleTouchMove);
      canvas.addEventListener("touchend", handleTouchEnd);
    };

    const handleDrawStart = (e) => {
      const rect = e.target.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      if (drawingMode.value === "shapes") {
        drawingState.isDrawing = true;
        drawingState.startX = x;
        drawingState.startY = y;
        drawingState.currentX = x;
        drawingState.currentY = y;
      } else if (drawingMode.value === "freehand") {
        isDrawing.value = true;
        freehandPoints.value = [{ x, y }];
      }
    };

    const handleDrawMove = (e) => {
      if (!isDrawing.value && !drawingState.isDrawing) return;

      const rect = e.target.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      if (drawingMode.value === "shapes" && drawingState.isDrawing) {
        drawingState.currentX = x;
        drawingState.currentY = y;
        drawPreviewShape(e.target);
      } else if (drawingMode.value === "freehand" && isDrawing.value) {
        freehandPoints.value.push({ x, y });
        drawFreehandPreview(e.target);
      }
    };

    const handleDrawEnd = (e) => {
      if (drawingMode.value === "shapes" && drawingState.isDrawing) {
        completeShapeDrawing();
        drawingState.isDrawing = false;
      } else if (drawingMode.value === "freehand" && isDrawing.value) {
        completeFreehandDrawing();
        isDrawing.value = false;
      }
    };

    const handleCanvasClick = (e) => {
      if (drawingMode.value === "text") {
        const rect = e.target.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        addTextAtPosition(x, y);
      }
    };

    const drawPreviewShape = (canvas) => {
      const ctx = canvas.getContext("2d");

      // Clear canvas and redraw all shapes
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      redrawAllShapes(ctx);

      // Draw preview shape
      ctx.strokeStyle = `rgb(${drawingColor.value.join(",")})`;
      ctx.lineWidth = drawingThickness.value;

      if (drawingFilled.value) {
        ctx.fillStyle = `rgb(${drawingColor.value.join(",")})`;
      }

      const startX = drawingState.startX;
      const startY = drawingState.startY;
      const currentX = drawingState.currentX;
      const currentY = drawingState.currentY;

      switch (currentDrawingTool.value) {
        case "rectangle":
          const width = currentX - startX;
          const height = currentY - startY;
          if (drawingFilled.value) {
            ctx.fillRect(startX, startY, width, height);
          } else {
            ctx.strokeRect(startX, startY, width, height);
          }
          break;

        case "circle":
          const radius = Math.sqrt(
            Math.pow(currentX - startX, 2) + Math.pow(currentY - startY, 2)
          );
          ctx.beginPath();
          ctx.arc(startX, startY, radius, 0, 2 * Math.PI);
          if (drawingFilled.value) {
            ctx.fill();
          } else {
            ctx.stroke();
          }
          break;

        case "line":
          ctx.beginPath();
          ctx.moveTo(startX, startY);
          ctx.lineTo(currentX, currentY);
          ctx.stroke();
          break;

        case "arrow":
          drawArrowPreview(ctx, startX, startY, currentX, currentY);
          break;
      }
    };

    const drawArrowPreview = (ctx, x1, y1, x2, y2) => {
      const headlen = 10;
      const dx = x2 - x1;
      const dy = y2 - y1;
      const angle = Math.atan2(dy, dx);

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.lineTo(
        x2 - headlen * Math.cos(angle - Math.PI / 6),
        y2 - headlen * Math.sin(angle - Math.PI / 6)
      );
      ctx.moveTo(x2, y2);
      ctx.lineTo(
        x2 - headlen * Math.cos(angle + Math.PI / 6),
        y2 - headlen * Math.sin(angle + Math.PI / 6)
      );
      ctx.stroke();
    };

    const completeShapeDrawing = () => {
      const shape = {
        type: currentDrawingTool.value,
        color: [...drawingColor.value],
        thickness: drawingThickness.value,
        filled: drawingFilled.value,
      };

      const startX = drawingState.startX;
      const startY = drawingState.startY;
      const currentX = drawingState.currentX;
      const currentY = drawingState.currentY;

      switch (currentDrawingTool.value) {
        case "rectangle":
          shape.x1 = startX;
          shape.y1 = startY;
          shape.x2 = currentX;
          shape.y2 = currentY;
          break;

        case "circle":
          shape.center_x = startX;
          shape.center_y = startY;
          shape.radius = Math.sqrt(
            Math.pow(currentX - startX, 2) + Math.pow(currentY - startY, 2)
          );
          break;

        case "line":
        case "arrow":
          shape.x1 = startX;
          shape.y1 = startY;
          shape.x2 = currentX;
          shape.y2 = currentY;
          if (currentDrawingTool.value === "arrow") {
            shape.tip_length = 0.1;
          }
          break;
      }

      currentShapes.value.push(shape);
      processDrawnShapes();
    };

    const drawFreehandPreview = (canvas) => {
      const ctx = canvas.getContext("2d");

      if (freehandPoints.value.length < 2) return;

      ctx.strokeStyle = `rgb(${drawingColor.value.join(",")})`;
      ctx.lineWidth = drawingThickness.value;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";

      ctx.beginPath();
      ctx.moveTo(freehandPoints.value[0].x, freehandPoints.value[0].y);

      for (let i = 1; i < freehandPoints.value.length; i++) {
        ctx.lineTo(freehandPoints.value[i].x, freehandPoints.value[i].y);
      }

      ctx.stroke();
    };

    const completeFreehandDrawing = () => {
      if (freehandPoints.value.length < 2) return;

      processFreehandDrawing();
    };

    const addTextAtPosition = (x, y) => {
      const text = prompt("Enter text to add:");
      if (!text) return;

      const fontSize = prompt("Enter font size (default: 1.0):", "1.0");
      const fontScale = parseFloat(fontSize) || 1.0;

      const textElement = {
        text,
        x: Math.round(x),
        y: Math.round(y),
        font_scale: fontScale,
        color: [...drawingColor.value],
        thickness: drawingThickness.value,
        font: "HERSHEY_SIMPLEX",
      };

      textElements.value.push(textElement);
      processTextElements();
    };

    const processDrawnShapes = async () => {
      if (!currentImage.value || currentShapes.value.length === 0) return;

      try {
        statusText.value = "Processing drawn shapes...";
        progress.value = 50;

        const base64Data = currentImage.value.split(",")[1];

        const result = await imageProcessingService.processImage(
          "draw-shapes",
          base64Data,
          { shapes: JSON.stringify(currentShapes.value) }
        );

        if (result.processed_image) {
          processedImage.value = `data:image/png;base64,${result.processed_image}`;
          processedInfo.operation = `Drawn ${
            result.shapes_drawn?.length || 0
          } shapes`;
          processedInfo.status = "Complete";

          statusText.value = `Drawn ${result.total_shapes || 0} shapes`;
          showMessage(
            `Successfully drew ${result.total_shapes || 0} shapes`,
            "success"
          );
        }

        progress.value = 100;
        setTimeout(() => {
          progress.value = 0;
          statusText.value = "Ready for more drawing";
        }, 1000);
      } catch (error) {
        console.error("Error processing shapes:", error);
        showMessage(`Error processing shapes: ${error.message}`, "error");
        statusText.value = "Drawing error";
        progress.value = 0;
      }
    };

    const processFreehandDrawing = async () => {
      if (!currentImage.value || freehandPoints.value.length === 0) return;

      try {
        statusText.value = "Processing freehand drawing...";
        progress.value = 50;

        const base64Data = currentImage.value.split(",")[1];

        const result = await imageProcessingService.processImage(
          "draw-freehand",
          base64Data,
          {
            points: JSON.stringify(freehandPoints.value),
            color: JSON.stringify(drawingColor.value),
            thickness: drawingThickness.value,
            closed: false,
          }
        );

        if (result.processed_image) {
          processedImage.value = `data:image/png;base64,${result.processed_image}`;
          processedInfo.operation = `Freehand drawing (${result.points_count} points)`;
          processedInfo.status = "Complete";

          statusText.value = `Freehand drawing with ${result.points_count} points`;
          showMessage("Freehand drawing completed", "success");
        }

        // Reset freehand points for next drawing
        freehandPoints.value = [];

        progress.value = 100;
        setTimeout(() => {
          progress.value = 0;
          statusText.value = "Ready for more drawing";
        }, 1000);
      } catch (error) {
        console.error("Error processing freehand:", error);
        showMessage(`Error processing freehand: ${error.message}`, "error");
        statusText.value = "Drawing error";
        progress.value = 0;
      }
    };

    const processTextElements = async () => {
      if (!currentImage.value || textElements.value.length === 0) return;

      try {
        statusText.value = "Processing text elements...";
        progress.value = 50;

        const base64Data = currentImage.value.split(",")[1];

        const result = await imageProcessingService.processImage(
          "draw-text-custom",
          base64Data,
          { text_elements: JSON.stringify(textElements.value) }
        );

        if (result.processed_image) {
          processedImage.value = `data:image/png;base64,${result.processed_image}`;
          processedInfo.operation = `Added ${
            result.texts_drawn?.length || 0
          } text elements`;
          processedInfo.status = "Complete";

          statusText.value = `Added ${result.total_texts || 0} text elements`;
          showMessage(
            `Successfully added ${result.total_texts || 0} text elements`,
            "success"
          );
        }

        progress.value = 100;
        setTimeout(() => {
          progress.value = 0;
          statusText.value = "Ready for more text";
        }, 1000);
      } catch (error) {
        console.error("Error processing text:", error);
        showMessage(`Error processing text: ${error.message}`, "error");
        statusText.value = "Text processing error";
        progress.value = 0;
      }
    };

    const redrawAllShapes = (ctx) => {
      // This would redraw all existing shapes on the canvas
      // Implementation depends on how you want to handle multiple shapes
    };

    const clearDrawing = () => {
      const canvas = document.getElementById("drawing-canvas");
      if (canvas) {
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }

      currentShapes.value = [];
      freehandPoints.value = [];
      textElements.value = [];
      statusText.value = "Drawing cleared";
    };

    const finishDrawing = () => {
      drawingMode.value = null;
      const canvas = document.getElementById("drawing-canvas");
      if (canvas) {
        canvas.remove();
      }

      statusText.value = "Drawing completed";
      showMessage("Drawing session finished", "success");
    };

    // Update parameters method to handle drawing tools
    const updateParameters = (operation, params) => {
      if (operation === "draw-shapes") {
        if (params.tool) currentDrawingTool.value = params.tool;
        if (params.color) drawingColor.value = params.color;
        if (params.thickness) drawingThickness.value = params.thickness;
        if (params.filled !== undefined) drawingFilled.value = params.filled;
      } else if (operation === "draw-freehand") {
        if (params.color) drawingColor.value = params.color;
        if (params.thickness) drawingThickness.value = params.thickness;
      } else if (operation === "add-text") {
        if (params.color) drawingColor.value = params.color;
        if (params.thickness) drawingThickness.value = params.thickness;
      } else {
        operationParameters[operation] = params;
        if (currentOperation.value === operation) {
          processImage(operation);
        }
      }
    };

    const closeControls = () => {
      showControls.value = false;
    };

    const toggleExportDropdown = () => {
      exportDropdownActive.value = !exportDropdownActive.value;
    };

    const exportAs = (format) => {
      if (!processedImage.value && !currentImage.value) {
        showMessage("No images to export", "error");
        return;
      }

      const imageToExport = processedImage.value || currentImage.value;
      const filename = `${
        currentOperation.value ? `processed_${currentOperation.value}` : "image"
      }_${Date.now()}`;

      if (format === "png") {
        downloadImage(imageToExport, `${filename}.png`);
      } else if (format === "jpg") {
        convertAndDownload(imageToExport, filename, "image/jpeg", ".jpg");
      }

      exportDropdownActive.value = false;
      showMessage(`Image exported as ${format.toUpperCase()}`, "success");
    };

    const downloadImage = (imageSrc, filename) => {
      const link = document.createElement("a");
      link.href = imageSrc;
      link.download = filename;
      link.click();
    };

    const convertAndDownload = (imageSrc, filename, mimeType, extension) => {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      const img = new Image();

      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;

        if (mimeType === "image/jpeg") {
          ctx.fillStyle = "white";
          ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        ctx.drawImage(img, 0, 0);

        canvas.toBlob(
          (blob) => {
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = filename + extension;
            link.click();
            URL.revokeObjectURL(link.href);
          },
          mimeType,
          0.9
        );
      };

      img.src = imageSrc;
    };

    const exportAsPDF = () => {
      if (!processedImage.value && !currentImage.value) {
        showMessage("No images to export", "error");
        return;
      }

      pdfModalActive.value = true;
      exportDropdownActive.value = false;
    };

    const exportAll = () => {
      if (!processedImage.value && !currentImage.value) {
        showMessage("No images to export", "error");
        return;
      }

      const timestamp = Date.now();
      const baseName = currentOperation.value
        ? `processed_${currentOperation.value}`
        : "image";

      const imageToExport = processedImage.value || currentImage.value;
      downloadImage(imageToExport, `${baseName}_${timestamp}.png`);

      setTimeout(() => {
        convertAndDownload(
          imageToExport,
          `${baseName}_${timestamp}`,
          "image/jpeg",
          ".jpg"
        );
      }, 500);

      setTimeout(() => {
        exportAsPDF();
      }, 1000);

      exportDropdownActive.value = false;
      showMessage("Exporting all formats...", "success");
    };

    const openBatchModal = () => {
      batchModalActive.value = true;
    };

    const closeBatchModal = () => {
      batchModalActive.value = false;
    };

    const handleBatchFiles = (files) => {
      batchFiles.value = [...batchFiles.value, ...files];
    };

    const removeBatchFile = (index) => {
      batchFiles.value.splice(index, 1);
    };

    // filepath: c:\Users\DELL\OneDrive\Desktop\ImageLab Studio\ImageLab Studio\src\App.vue
    const startBatchProcessing = async (operationData) => {
      if (!operationData || !operationData.operation) {
        showMessage("Please select an operation first", "error");
        return;
      }

      if (batchFiles.value.length === 0) {
        showMessage("No files selected for batch processing", "error");
        return;
      }

      try {
        statusText.value = "Starting batch processing...";
        progress.value = 0;

        console.log("Starting batch with operation:", operationData.operation);
        console.log("Parameters:", operationData.parameters);

        // Ensure we have the current parameters for the operation
        const currentParams =
          operationParameters[operationData.operation] ||
          operationData.parameters ||
          {};

        console.log("Using parameters:", currentParams);

        const result = await imageProcessingService.batchProcess(
          batchFiles.value,
          operationData.operation,
          currentParams
        );

        if (result.results) {
          const successCount = result.total_processed || 0;
          const failCount = result.total_failed || 0;

          statusText.value = `Batch complete: ${successCount} success, ${failCount} failed`;

          // Show detailed results if available
          if (result.results.length > 0) {
            console.log("Batch results:", result.results);
            showMessage(
              `Batch processing completed: ${successCount} images processed with ${operationData.operation}, ${failCount} failed`,
              successCount > 0 ? "success" : "error"
            );
          }

          // Reset batch processing
          batchFiles.value = [];
          closeBatchModal();
          progress.value = 100;

          setTimeout(() => {
            progress.value = 0;
            statusText.value = "Ready";
          }, 3000);
        }
      } catch (error) {
        console.error("Batch processing failed:", error);
        statusText.value = "Batch processing failed";
        showMessage(`Batch processing failed: ${error.message}`, "error");
        progress.value = 0;
      }
    };

    const closePDFModal = () => {
      pdfModalActive.value = false;
    };

    const generatePDFReport = async (options) => {
      try {
        statusText.value = "Generating PDF report...";
        progress.value = 30;

        const pdf = new jsPDF("p", "mm", "a4");
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        let yPosition = 20;

        // Add title
        pdf.setFontSize(20);
        pdf.setFont("helvetica", "bold");
        pdf.text(
          options.title || "Image Processing Report",
          pageWidth / 2,
          yPosition,
          { align: "center" }
        );
        yPosition += 15;

        // Add date
        pdf.setFontSize(12);
        pdf.setFont("helvetica", "normal");
        const currentDate = new Date().toLocaleDateString();
        pdf.text(`Generated on: ${currentDate}`, 20, yPosition);
        yPosition += 15;

        // Add operation details if enabled
        if (options.includeDetails && currentOperation.value) {
          pdf.setFontSize(14);
          pdf.setFont("helvetica", "bold");
          pdf.text("Processing Details:", 20, yPosition);
          yPosition += 10;

          pdf.setFontSize(12);
          pdf.setFont("helvetica", "normal");
          pdf.text(`Operation: ${currentOperation.value}`, 25, yPosition);
          yPosition += 8;

          // Add parameters if available
          const params = operationParameters[currentOperation.value];
          if (params && Object.keys(params).length > 0) {
            pdf.text("Parameters:", 25, yPosition);
            yPosition += 6;
            Object.entries(params).forEach(([key, value]) => {
              pdf.text(`  ${key}: ${value}`, 30, yPosition);
              yPosition += 6;
            });
          }
          yPosition += 10;
        }

        progress.value = 50;

        // Add original image if enabled and available
        if (options.includeOriginal && currentImage.value) {
          if (yPosition > pageHeight - 80) {
            pdf.addPage();
            yPosition = 20;
          }

          pdf.setFontSize(14);
          pdf.setFont("helvetica", "bold");
          pdf.text("Original Image:", 20, yPosition);
          yPosition += 10;

          try {
            // Convert image to canvas and add to PDF
            const originalCanvas = await createImageCanvas(currentImage.value);
            const originalImgData = originalCanvas.toDataURL("image/png");

            const imgWidth = 150;
            const imgHeight =
              (originalCanvas.height * imgWidth) / originalCanvas.width;

            pdf.addImage(
              originalImgData,
              "PNG",
              20,
              yPosition,
              imgWidth,
              imgHeight
            );
            yPosition += imgHeight + 15;
          } catch (error) {
            console.error("Error adding original image:", error);
            pdf.text("Error loading original image", 25, yPosition);
            yPosition += 10;
          }
        }

        progress.value = 70;

        // Add processed image if enabled and available
        if (options.includeProcessed && processedImage.value) {
          if (yPosition > pageHeight - 80) {
            pdf.addPage();
            yPosition = 20;
          }

          pdf.setFontSize(14);
          pdf.setFont("helvetica", "bold");
          pdf.text("Processed Image:", 20, yPosition);
          yPosition += 10;

          try {
            const processedCanvas = await createImageCanvas(
              processedImage.value
            );
            const processedImgData = processedCanvas.toDataURL("image/png");

            const imgWidth = 150;
            const imgHeight =
              (processedCanvas.height * imgWidth) / processedCanvas.width;

            pdf.addImage(
              processedImgData,
              "PNG",
              20,
              yPosition,
              imgWidth,
              imgHeight
            );
            yPosition += imgHeight + 15;
          } catch (error) {
            console.error("Error adding processed image:", error);
            pdf.text("Error loading processed image", 25, yPosition);
            yPosition += 10;
          }
        }

        // Add metadata if enabled
        if (options.includeMetadata) {
          if (yPosition > pageHeight - 40) {
            pdf.addPage();
            yPosition = 20;
          }

          pdf.setFontSize(14);
          pdf.setFont("helvetica", "bold");
          pdf.text("Image Information:", 20, yPosition);
          yPosition += 10;

          pdf.setFontSize(12);
          pdf.setFont("helvetica", "normal");

          if (originalInfo.width && originalInfo.height) {
            pdf.text(
              `Original Dimensions: ${originalInfo.width} x ${originalInfo.height}`,
              25,
              yPosition
            );
            yPosition += 8;
          }

          if (originalInfo.fileSize) {
            pdf.text(`File Size: ${originalInfo.fileSize}`, 25, yPosition);
            yPosition += 8;
          }

          if (originalInfo.format) {
            pdf.text(`Format: ${originalInfo.format}`, 25, yPosition);
            yPosition += 8;
          }

          yPosition += 5;
        }

        // Add notes if provided
        if (options.notes && options.notes.trim()) {
          if (yPosition > pageHeight - 30) {
            pdf.addPage();
            yPosition = 20;
          }

          pdf.setFontSize(14);
          pdf.setFont("helvetica", "bold");
          pdf.text("Notes:", 20, yPosition);
          yPosition += 10;

          pdf.setFontSize(12);
          pdf.setFont("helvetica", "normal");

          // Split long notes into multiple lines
          const splitNotes = pdf.splitTextToSize(options.notes, pageWidth - 40);
          pdf.text(splitNotes, 25, yPosition);
        }

        progress.value = 90;

        // Generate filename and save
        const timestamp = new Date()
          .toISOString()
          .slice(0, 19)
          .replace(/:/g, "-");
        const filename = `ImageLab_Report_${timestamp}.pdf`;

        pdf.save(filename);

        progress.value = 100;
        statusText.value = "PDF report generated successfully";
        showMessage(
          "PDF report generated and downloaded successfully",
          "success"
        );

        // Reset progress after a delay
        setTimeout(() => {
          progress.value = 0;
          statusText.value = "Ready";
        }, 2000);

        closePDFModal();
      } catch (error) {
        console.error("PDF generation error:", error);
        statusText.value = "PDF generation failed";
        showMessage(`PDF generation failed: ${error.message}`, "error");
        progress.value = 0;
      }
    };

    // Helper function to create canvas from image
    const createImageCanvas = (imageSrc) => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.crossOrigin = "anonymous";

        img.onload = () => {
          const canvas = document.createElement("canvas");
          const ctx = canvas.getContext("2d");

          // Set canvas dimensions
          canvas.width = img.width;
          canvas.height = img.height;

          // Draw image to canvas
          ctx.drawImage(img, 0, 0);

          resolve(canvas);
        };

        img.onerror = () => {
          reject(new Error("Failed to load image"));
        };

        img.src = imageSrc;
      });
    };

    const showMessage = (message, type) => {
      // Simple toast notification implementation
      const messageDiv = document.createElement("div");
      messageDiv.className = `toast toast-${type}`;
      messageDiv.textContent = message;
      messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        transition: all 0.3s ease;
        ${
          type === "error"
            ? "background-color: #e74c3c;"
            : "background-color: #27ae60;"
        }
      `;

      document.body.appendChild(messageDiv);

      setTimeout(() => {
        if (document.body.contains(messageDiv)) {
          document.body.removeChild(messageDiv);
        }
      }, 3000);
    };

    // Lifecycle
    onMounted(() => {
      checkBackendConnection();

      // Setup keyboard shortcuts
      document.addEventListener("keydown", (e) => {
        if (e.ctrlKey || e.metaKey) {
          switch (e.key) {
            case "o":
              e.preventDefault();
              document.querySelector('input[type="file"]').click();
              break;
            case "s":
              e.preventDefault();
              toggleExportDropdown();
              break;
            case "b":
              e.preventDefault();
              openBatchModal();
              break;
            case "p":
              e.preventDefault();
              exportAsPDF();
              break;
          }
        }
      });
    });

    return {
      // Data
      currentImage,
      processedImage,
      currentOperation,
      showControls,
      backendConnected,
      backendStatus,
      statusText,
      progress,
      imageCount,
      exportDropdownActive,
      batchModalActive,
      pdfModalActive,
      originalInfo,
      processedInfo,
      batchFiles,
      showStatusModal,
      toggleStatusModal,
      closeStatusModal,
      drawingMode,
      currentShapes,
      freehandPoints,
      textElements,
      isDrawing,
      currentDrawingTool,
      drawingColor,
      drawingThickness,
      drawingFilled,
      availableTools,
      selectDrawingTool,
      rgbToHex,
      updateColor,
      selectRGBChannel,
      extractRedChannel,
      extractGreenChannel,
      extractBlueChannel,

      // Methods
      handleImageLoad,
      selectOperation,
      closeControls,
      updateParameters,
      toggleExportDropdown,
      exportAs,
      exportAsPDF,
      exportAll,
      openBatchModal,
      closeBatchModal,
      handleBatchFiles,
      removeBatchFile,
      startBatchProcessing,
      closePDFModal,
      generatePDFReport,
      initializeDrawingMode,
      clearDrawing,
      finishDrawing,
    };
  },
};
</script>
