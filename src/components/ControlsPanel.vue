<template>
  <div class="controls-panel active">
    <div class="controls-header">
      <h4>Processing Controls</h4>
      <button class="icon-btn" @click="$emit('close')">
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <line x1="18" y1="6" x2="6" y2="18" />
          <line x1="6" y1="6" x2="18" y2="18" />
        </svg>
      </button>
    </div>

    <div class="controls-content">
      <h3>Controls: {{ operation.replace(/-/g, " ").toUpperCase() }}</h3>

      <!-- Rotation Controls -->
      <template v-if="operation === 'rotate'">
        <div class="control-group">
          <label
            >Rotation Angle: <span>{{ params.angle }}°</span></label
          >
          <input
            type="range"
            min="0"
            max="360"
            v-model="params.angle"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label
            >Scale Factor: <span>{{ params.scale }}</span></label
          >
          <input
            type="range"
            min="0.1"
            max="2.0"
            step="0.1"
            v-model="params.scale"
            @input="updateParams"
          />
        </div>
      </template>

      <!-- Blur Controls -->
      <template v-if="operation === 'blur'">
        <div class="control-group">
          <label>Blur Type</label>
          <select v-model="params.blur_type" @change="updateParams">
            <option value="gaussian">Gaussian Blur</option>
            <option value="motion">Motion Blur</option>
            <option value="median">Median Filter</option>
            <option value="bilateral">Bilateral Filter</option>
          </select>
        </div>
        <div class="control-group">
          <label
            >Kernel Size: <span>{{ params.kernel_size }}</span></label
          >
          <input
            type="range"
            min="3"
            max="31"
            step="2"
            v-model="params.kernel_size"
            @input="updateParams"
          />
        </div>
      </template>

      <!-- Threshold Controls -->
      <template v-if="operation === 'threshold'">
        <div class="control-group">
          <label
            >Threshold Value: <span>{{ params.threshold_value }}</span></label
          >
          <input
            type="range"
            min="0"
            max="255"
            v-model="params.threshold_value"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label>Threshold Type</label>
          <select v-model="params.threshold_type" @change="updateParams">
            <option value="binary">Binary</option>
            <option value="binary_inv">Binary Inverted</option>
            <option value="trunc">Truncate</option>
            <option value="tozero">To Zero</option>
            <option value="tozero_inv">To Zero Inverted</option>
          </select>
        </div>
      </template>

      <!-- Resize Controls -->
      <template v-if="operation === 'resize'">
        <div class="control-group">
          <label
            >Scale Factor: <span>{{ params.scale_factor }}x</span></label
          >
          <input
            type="range"
            min="0.1"
            max="2.0"
            step="0.1"
            v-model="params.scale_factor"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label>Interpolation Method</label>
          <select v-model="params.interpolation" @change="updateParams">
            <option value="linear">Linear</option>
            <option value="cubic">Cubic</option>
            <option value="nearest">Nearest Neighbor</option>
            <option value="lanczos">Lanczos</option>
          </select>
        </div>
      </template>

      <!-- Edge Detection Controls -->
      <template v-if="operation === 'edge-detection'">
        <div class="control-group">
          <label
            >Lower Threshold: <span>{{ params.low_threshold }}</span></label
          >
          <input
            type="range"
            min="0"
            max="255"
            v-model="params.low_threshold"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label
            >Upper Threshold: <span>{{ params.high_threshold }}</span></label
          >
          <input
            type="range"
            min="0"
            max="255"
            v-model="params.high_threshold"
            @input="updateParams"
          />
        </div>
      </template>

      <!-- Color Manipulation Controls -->
      <template v-if="operation === 'color-manipulation'">
        <div class="control-group">
          <label
            >Hue Shift: <span>{{ params.hue_shift }}</span></label
          >
          <input
            type="range"
            min="-180"
            max="180"
            v-model="params.hue_shift"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label
            >Saturation: <span>{{ params.saturation_factor }}</span></label
          >
          <input
            type="range"
            min="0"
            max="3"
            step="0.1"
            v-model="params.saturation_factor"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label
            >Value/Brightness: <span>{{ params.value_factor }}</span></label
          >
          <input
            type="range"
            min="0"
            max="3"
            step="0.1"
            v-model="params.value_factor"
            @input="updateParams"
          />
        </div>
      </template>

      <!-- Crop Controls -->
      <template v-if="operation === 'crop'">
        <div class="control-group">
          <label
            >X Position: <span>{{ params.x }}</span></label
          >
          <input
            type="range"
            min="0"
            max="500"
            v-model="params.x"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label
            >Y Position: <span>{{ params.y }}</span></label
          >
          <input
            type="range"
            min="0"
            max="500"
            v-model="params.y"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label
            >Width: <span>{{ params.width }}</span></label
          >
          <input
            type="range"
            min="50"
            max="400"
            v-model="params.width"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label
            >Height: <span>{{ params.height }}</span></label
          >
          <input
            type="range"
            min="50"
            max="400"
            v-model="params.height"
            @input="updateParams"
          />
        </div>
      </template>

      <!-- Arithmetic Controls -->
      <template v-if="operation === 'arithmetic'">
        <div class="control-group">
          <label>Operation</label>
          <select v-model="params.operation" @change="updateParams">
            <option value="add">Add</option>
            <option value="subtract">Subtract</option>
            <option value="multiply">Multiply</option>
            <option value="divide">Divide</option>
          </select>
        </div>
        <div class="control-group">
          <label
            >Value: <span>{{ params.value }}</span></label
          >
          <input
            type="range"
            min="1"
            max="200"
            v-model="params.value"
            @input="updateParams"
          />
        </div>
      </template>

      <!-- Bitwise Controls -->
      <template v-if="operation === 'bitwise'">
        <div class="control-group">
          <label>Operation</label>
          <select v-model="params.operation" @change="updateParams">
            <option value="and">AND</option>
            <option value="or">OR</option>
            <option value="xor">XOR</option>
            <option value="not">NOT</option>
          </select>
        </div>
        <div class="control-group">
          <label>Mask Type</label>
          <select v-model="params.mask_type" @change="updateParams">
            <option value="circular">Circular</option>
            <option value="rectangular">Rectangular</option>
            <option value="full">Full</option>
          </select>
        </div>
      </template>

      <!-- Morphological Controls -->
      <template
        v-if="['dilation', 'erosion', 'opening', 'closing'].includes(operation)"
      >
        <div class="control-group">
          <label
            >Kernel Size: <span>{{ params.kernel_size }}</span></label
          >
          <input
            type="range"
            min="3"
            max="15"
            step="2"
            v-model="params.kernel_size"
            @input="updateParams"
          />
        </div>
        <div class="control-group">
          <label
            >Iterations: <span>{{ params.iterations }}</span></label
          >
          <input
            type="range"
            min="1"
            max="5"
            v-model="params.iterations"
            @input="updateParams"
          />
        </div>
      </template>

      <!-- Default message for operations without controls -->
      <template v-if="!hasControls">
        <p>No additional controls needed for this operation.</p>
      </template>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from "vue";

export default {
  name: "ControlsPanel",
  props: {
    operation: {
      type: String,
      required: true,
    },
  },
  emits: ["close", "update"],
  setup(props, { emit }) {
    // Default parameters for each operation
    const defaultParams = {
      rotate: { angle: 45, scale: 1.0 },
      blur: { blur_type: "gaussian", kernel_size: 15 },
      threshold: { threshold_value: 127, threshold_type: "binary" },
      resize: { scale_factor: 0.5, interpolation: "linear" },
      "edge-detection": { low_threshold: 50, high_threshold: 150 },
      "color-manipulation": {
        hue_shift: 0,
        saturation_factor: 1.0,
        value_factor: 1.0,
      },
      crop: { x: 100, y: 100, width: 200, height: 200 },
      arithmetic: { operation: "add", value: 50 },
      bitwise: { operation: "and", mask_type: "circular" },
      dilation: { kernel_size: 5, iterations: 1 },
      erosion: { kernel_size: 5, iterations: 1 },
      opening: { kernel_size: 5, iterations: 1 },
      closing: { kernel_size: 5, iterations: 1 },
    };

    const params = ref(defaultParams[props.operation] || {});

    const hasControls = computed(() => {
      return Object.keys(defaultParams).includes(props.operation);
    });

    const updateParams = () => {
      emit("update", props.operation, params.value);
    };

    // Watch for operation changes
    watch(
      () => props.operation,
      (newOperation) => {
        params.value = defaultParams[newOperation] || {};
        updateParams();
      },
      { immediate: true }
    );

    return {
      params,
      hasControls,
      updateParams,
    };
  },
};
</script>
