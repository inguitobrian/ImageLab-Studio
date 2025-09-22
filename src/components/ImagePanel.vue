<template>
  <div class="image-panel">
    <div class="panel-header">
      <h3>{{ title }}</h3>
      <div class="panel-actions">
        <button class="icon-btn" @click="downloadImage" v-if="image">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7,10 12,15 17,10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
        </button>
        <button class="icon-btn" @click="viewFullscreen" v-if="image">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
            <circle cx="12" cy="12" r="3" />
          </svg>
        </button>
      </div>
    </div>

    <div class="image-display" :class="{ processing: isProcessing }">
      <img v-if="image" :src="image" :alt="title" />
      <div v-else class="placeholder-content">
        <div class="placeholder-icon">
          <svg
            v-if="!isProcessed"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
            <circle cx="8.5" cy="8.5" r="1.5" />
            <polyline points="21,15 16,10 5,21" />
          </svg>
          <svg
            v-else
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <path
              d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"
            />
          </svg>
        </div>
        <h4 v-if="!isProcessed">Load an image to get started</h4>
        <h4 v-else>Select an operation</h4>
        <p v-if="!isProcessed">Supports JPG, PNG, BMP, TIFF formats</p>
        <p v-else>
          Choose a processing operation from the sidebar to see results
        </p>
        <button
          v-if="!isProcessed"
          class="btn btn-outline"
          @click="$emit('load-image')"
        >
          Choose File
        </button>
      </div>
    </div>

    <div class="image-info">
      <div class="info-grid">
        <div class="info-item" v-if="info.status">
          <span class="info-label">Status</span>
          <span class="info-value">{{ info.status }}</span>
        </div>
        <div class="info-item" v-if="info.filename">
          <span class="info-label">File</span>
          <span class="info-value">{{ info.filename }}</span>
        </div>
        <div class="info-item" v-if="info.size">
          <span class="info-label">Size</span>
          <span class="info-value">{{ info.size }}</span>
        </div>
        <div class="info-item" v-if="info.dimensions">
          <span class="info-label">Dimensions</span>
          <span class="info-value">{{ info.dimensions }}</span>
        </div>
        <div class="info-item" v-if="info.type">
          <span class="info-label">Type</span>
          <span class="info-value">{{ info.type }}</span>
        </div>
        <div class="info-item" v-if="info.operation">
          <span class="info-label">Operation</span>
          <span class="info-value">{{ info.operation }}</span>
        </div>
        <div class="info-item" v-if="info.backend">
          <span class="info-label">Backend</span>
          <span class="info-value">{{ info.backend }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ImagePanel",
  props: {
    title: {
      type: String,
      required: true,
    },
    image: {
      type: String,
      default: null,
    },
    info: {
      type: Object,
      default: () => ({}),
    },
    isProcessed: {
      type: Boolean,
      default: false,
    },
    isProcessing: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["load-image"],
  methods: {
    downloadImage() {
      if (this.image) {
        const link = document.createElement("a");
        link.href = this.image;
        link.download = `${this.title
          .toLowerCase()
          .replace(" ", "_")}_${Date.now()}.png`;
        link.click();
      }
    },
    viewFullscreen() {
      if (this.image) {
        // Simple fullscreen implementation
        const modal = document.createElement("div");
        modal.style.cssText = `
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          background: rgba(0,0,0,0.9);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 10000;
          cursor: pointer;
        `;

        const img = document.createElement("img");
        img.src = this.image;
        img.style.cssText = `
          max-width: 90vw;
          max-height: 90vh;
          object-fit: contain;
        `;

        modal.appendChild(img);
        modal.onclick = () => document.body.removeChild(modal);
        document.body.appendChild(modal);
      }
    },
  },
};
</script>
