<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Batch Processing</h3>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>

      <div class="modal-body">
        <!-- Operation Selection -->
        <div class="operation-selection">
          <h4>Select Operation</h4>
          <div class="operation-grid">
            <div
              v-for="operation in availableOperations"
              :key="operation.id"
              class="operation-card"
              :class="{ active: selectedOperation === operation.id }"
              @click="selectOperation(operation.id)"
            >
              <span class="operation-icon">{{ operation.icon }}</span>
              <span class="operation-name">{{ operation.name }}</span>
            </div>
          </div>
        </div>

        <!-- Parameters Panel (if operation selected) -->
        <div v-if="selectedOperation" class="parameters-panel">
          <h4>Parameters</h4>
          <div class="parameter-controls">
            <!-- Grayscale (no parameters) -->
            <div v-if="selectedOperation === 'grayscale'">
              <p class="parameter-info">No additional parameters required.</p>
            </div>

            <!-- Blur Parameters -->
            <div
              v-else-if="selectedOperation === 'blur'"
              class="parameter-group"
            >
              <label>Blur Type:</label>
              <select v-model="parameters.blur_type">
                <option value="gaussian">Gaussian</option>
                <option value="median">Median</option>
                <option value="bilateral">Bilateral</option>
              </select>

              <label>Kernel Size:</label>
              <input
                type="range"
                v-model="parameters.kernel_size"
                min="3"
                max="31"
                step="2"
              />
              <span>{{ parameters.kernel_size }}</span>
            </div>

            <!-- Resize Parameters -->
            <div
              v-else-if="selectedOperation === 'resize'"
              class="parameter-group"
            >
              <label>Scale Factor:</label>
              <input
                type="range"
                v-model="parameters.scale_factor"
                min="0.1"
                max="2.0"
                step="0.1"
              />
              <span>{{ parameters.scale_factor }}</span>

              <label>Interpolation:</label>
              <select v-model="parameters.interpolation">
                <option value="linear">Linear</option>
                <option value="cubic">Cubic</option>
                <option value="nearest">Nearest</option>
              </select>
            </div>

            <!-- Rotate Parameters -->
            <div
              v-else-if="selectedOperation === 'rotate'"
              class="parameter-group"
            >
              <label>Angle:</label>
              <input
                type="range"
                v-model="parameters.angle"
                min="-180"
                max="180"
                step="1"
              />
              <span>{{ parameters.angle }}°</span>

              <label>Scale:</label>
              <input
                type="range"
                v-model="parameters.scale"
                min="0.1"
                max="2.0"
                step="0.1"
              />
              <span>{{ parameters.scale }}</span>
            </div>

            <!-- Edge Detection Parameters -->
            <div
              v-else-if="selectedOperation === 'detect-edges'"
              class="parameter-group"
            >
              <label>Low Threshold:</label>
              <input
                type="range"
                v-model="parameters.low_threshold"
                min="0"
                max="255"
                step="1"
              />
              <span>{{ parameters.low_threshold }}</span>

              <label>High Threshold:</label>
              <input
                type="range"
                v-model="parameters.high_threshold"
                min="0"
                max="255"
                step="1"
              />
              <span>{{ parameters.high_threshold }}</span>
            </div>

            <!-- Threshold Parameters -->
            <div
              v-else-if="selectedOperation === 'threshold'"
              class="parameter-group"
            >
              <label>Threshold Value:</label>
              <input
                type="range"
                v-model="parameters.threshold_value"
                min="0"
                max="255"
                step="1"
              />
              <span>{{ parameters.threshold_value }}</span>

              <label>Threshold Type:</label>
              <select v-model="parameters.threshold_type">
                <option value="binary">Binary</option>
                <option value="binary_inv">Binary Inverted</option>
                <option value="trunc">Truncated</option>
                <option value="tozero">To Zero</option>
                <option value="tozero_inv">To Zero Inverted</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Export Settings -->
        <div v-if="selectedOperation" class="export-settings">
          <h4>Export Settings</h4>
          <div class="export-controls">
            <label>Output Format:</label>
            <select v-model="exportSettings.format">
              <option value="png">PNG</option>
              <option value="jpg">JPG</option>
            </select>

            <div v-if="exportSettings.format === 'jpg'" class="quality-setting">
              <label>JPG Quality:</label>
              <input
                type="range"
                v-model="exportSettings.quality"
                min="10"
                max="100"
                step="5"
              />
              <span>{{ exportSettings.quality }}%</span>
            </div>

            <label>File Naming:</label>
            <input
              type="text"
              v-model="exportSettings.prefix"
              placeholder="processed_"
              class="prefix-input"
            />
            <small>Files will be named: [prefix][original_name].[format]</small>
          </div>
        </div>

        <!-- File Drop Zone -->
        <div
          class="file-drop-zone"
          @drop="handleDrop"
          @dragover.prevent
          @dragenter.prevent
        >
          <input
            type="file"
            ref="fileInput"
            multiple
            accept="image/*"
            @change="handleFileSelect"
            style="display: none"
          />
          <p>
            Drop images here or
            <button class="browse-btn" @click="$refs.fileInput.click()">
              click to select
            </button>
          </p>
          <small>Supports JPG, PNG, BMP, TIFF</small>
        </div>

        <!-- File List -->
        <div v-if="files.length > 0" class="file-list">
          <h4>Selected Files ({{ files.length }})</h4>
          <div class="file-items">
            <div v-for="(file, index) in files" :key="index" class="file-item">
              <span class="file-name">{{ file.name }}</span>
              <span class="file-size">({{ formatFileSize(file.size) }})</span>
              <button class="remove-btn" @click="$emit('remove-file', index)">
                Remove
              </button>
            </div>
          </div>
        </div>

        <!-- Processing Status -->
        <div v-if="isProcessing" class="processing-status">
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: processingProgress + '%' }"
            ></div>
          </div>
          <p>Processing {{ currentFile }}/{{ totalFiles }}...</p>
        </div>

        <!-- Processing Results -->
        <div v-if="processedImages.length > 0" class="processing-results">
          <h4>Processing Complete ({{ processedImages.length }} images)</h4>
          <button
            class="btn btn-success export-btn"
            @click="exportAsZip"
            :disabled="isExporting"
          >
            {{ isExporting ? "Exporting..." : "Download as ZIP" }}
          </button>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary" @click="$emit('close')">
          Cancel
        </button>
        <button
          class="btn btn-primary"
          @click="startProcessing"
          :disabled="!selectedOperation || files.length === 0 || isProcessing"
        >
          {{ isProcessing ? "Processing..." : "Start Processing" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import JSZip from "jszip"; // You'll need to install this: npm install jszip
import { imageProcessingService } from "../services/ImageProcessingService";
export default {
  props: {
    files: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["close", "add-files", "remove-file", "start-processing"],
  data() {
    return {
      selectedOperation: null,
      parameters: {},
      exportSettings: {
        format: "png",
        quality: 90,
        prefix: "processed_",
      },
      isProcessing: false,
      isExporting: false,
      processingProgress: 0,
      currentFile: 0,
      totalFiles: 0,
      processedImages: [],
      availableOperations: [
        { id: "grayscale", name: "Convert to Grayscale", icon: "⚫" },
        { id: "blur", name: "Blur Image", icon: "🌫️" },
        { id: "resize", name: "Resize Image", icon: "📏" },
        { id: "rotate", name: "Rotate Image", icon: "🔄" },
        { id: "detect-edges", name: "Edge Detection", icon: "🔍" },
        { id: "threshold", name: "Threshold", icon: "📊" },
        { id: "rgb-channels", name: "RGB Channels", icon: "🌈" },
        { id: "hsv-convert", name: "HSV Conversion", icon: "🎨" },
        { id: "flip", name: "Flip Image", icon: "↔️" },
        { id: "crop", name: "Crop Image", icon: "✂️" },
      ],
    };
  },
  methods: {
    selectOperation(operationId) {
      this.selectedOperation = operationId;
      this.initializeParameters(operationId);
    },
    initializeParameters(operation) {
      const defaults = {
        blur: { blur_type: "gaussian", kernel_size: 15 },
        resize: { scale_factor: 0.5, interpolation: "linear" },
        rotate: { angle: 45, scale: 1.0 },
        "detect-edges": { low_threshold: 50, high_threshold: 150 },
        threshold: { threshold_value: 127, threshold_type: "binary" },
        flip: { flip_code: 1 },
        crop: { x: 100, y: 100, width: 200, height: 200 },
      };
      this.parameters = { ...defaults[operation] } || {};
    },
    handleFileSelect(event) {
      const newFiles = Array.from(event.target.files);
      this.$emit("add-files", newFiles);
    },
    handleDrop(event) {
      event.preventDefault();
      const newFiles = Array.from(event.dataTransfer.files);
      this.$emit("add-files", newFiles);
    },
    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
    },
    async startProcessing() {
      this.isProcessing = true;
      this.processedImages = [];
      this.totalFiles = this.files.length;
      this.currentFile = 0;
      this.processingProgress = 0;

      try {
        // Process each file
        for (let i = 0; i < this.files.length; i++) {
          this.currentFile = i + 1;
          const file = this.files[i];

          // Process the image (you'll need to implement the actual processing logic)
          const processedImageData = await this.processImage(file);

          this.processedImages.push({
            originalName: file.name,
            data: processedImageData,
            name: this.generateFileName(file.name),
          });

          this.processingProgress = ((i + 1) / this.files.length) * 100;
        }
      } catch (error) {
        console.error("Processing error:", error);
        alert("An error occurred during processing");
      } finally {
        this.isProcessing = false;
      }
    },
    async processImage(file) {
      // This is a placeholder - you'll need to implement actual image processing
      // based on the selected operation and parameters
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          // Here you would apply the selected operation with parameters
          // For now, just return the original image data
          resolve(e.target.result);
        };
        reader.readAsDataURL(file);
      });
    },
    generateFileName(originalName) {
      const nameWithoutExt = originalName.split(".").slice(0, -1).join(".");
      return `${this.exportSettings.prefix}${nameWithoutExt}.${this.exportSettings.format}`;
    },
    async exportAsZip() {
      this.isExporting = true;

      try {
        const zip = new JSZip();

        // Add each processed image to the zip
        for (const image of this.processedImages) {
          // Convert data URL to blob
          const blob = await this.dataURLToBlob(image.data);
          zip.file(image.name, blob);
        }

        // Generate zip file
        const zipBlob = await zip.generateAsync({ type: "blob" });

        // Download the zip file
        const url = URL.createObjectURL(zipBlob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `batch_processed_${
          this.selectedOperation
        }_${Date.now()}.zip`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } catch (error) {
        console.error("Export error:", error);
        alert("An error occurred during export");
      } finally {
        this.isExporting = false;
      }
    },
    async dataURLToBlob(dataURL) {
      const response = await fetch(dataURL);
      return response.blob();
    },
    async processImage(file) {
      try {
        // Convert file to base64
        const base64Data = await this.fileToBase64(file);

        // Use the ImageProcessingService to actually process the image
        const result = await imageProcessingService.processImage(
          this.selectedOperation,
          base64Data,
          this.parameters
        );

        // Return the processed image data
        if (result.processed_image) {
          return `data:image/png;base64,${result.processed_image}`;
        } else if (result.red_channel) {
          // Handle RGB channels case
          return `data:image/png;base64,${result.red_channel}`;
        } else if (result.hsv_image) {
          // Handle HSV conversion case
          return `data:image/png;base64,${result.hsv_image}`;
        } else {
          // Fallback to original if processing fails
          return await this.fileToDataURL(file);
        }
      } catch (error) {
        console.error("Error processing image:", error);
        // Return original image if processing fails
        return await this.fileToDataURL(file);
      }
    },

    // Helper method to convert file to base64 (add this if not already present)
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
    },

    // Helper method to convert file to data URL
    fileToDataURL(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    },
  },
};
</script>

<style scoped>
/* ...existing styles... */

.export-settings {
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.export-controls {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.export-controls label {
  font-weight: bold;
  margin-bottom: 5px;
}

.export-controls select,
.prefix-input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.quality-setting {
  display: flex;
  align-items: center;
  gap: 10px;
}

.processing-status {
  margin: 20px 0;
  text-align: center;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  background-color: #4caf50;
  transition: width 0.3s ease;
}

.processing-results {
  margin: 20px 0;
  text-align: center;
  padding: 15px;
  background-color: #e8f5e8;
  border-radius: 8px;
}

.export-btn {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
}

.btn-success {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-success:hover:not(:disabled) {
  background-color: #218838;
}

.btn-success:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>
