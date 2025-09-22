<template>
  <div class="modal-overlay">
    <div class="modal">
      <div class="modal-header">
        <h2>Generate PDF Report</h2>
        <button class="icon-btn" @click="$emit('close')">
          <svg
            width="20"
            height="20"
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

      <div class="modal-body">
        <p class="modal-description">Configure your PDF report settings</p>

        <div class="control-group">
          <label>Report Title</label>
          <input
            type="text"
            v-model="reportOptions.title"
            class="control-input"
            placeholder="Enter report title"
          />
        </div>

        <div class="control-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="reportOptions.includeOriginal" />
            Include Original Image
          </label>
        </div>

        <div class="control-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="reportOptions.includeProcessed" />
            Include Processed Image
          </label>
        </div>

        <div class="control-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="reportOptions.includeDetails" />
            Include Processing Details
          </label>
        </div>

        <div class="control-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="reportOptions.includeMetadata" />
            Include Metadata
          </label>
        </div>

        <div class="control-group">
          <label>Additional Notes</label>
          <textarea
            v-model="reportOptions.notes"
            placeholder="Add any additional notes..."
            rows="3"
            class="control-input"
          >
          </textarea>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-outline" @click="$emit('close')">Cancel</button>
        <button class="btn btn-primary" @click="generateReport">
          Generate PDF
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from "vue";

export default {
  name: "PDFModal",
  emits: ["close", "generate"],
  setup(props, { emit }) {
    const reportOptions = reactive({
      title: "Image Processing Report",
      includeOriginal: true,
      includeProcessed: true,
      includeDetails: true,
      includeMetadata: true,
      notes: "",
    });

    const generateReport = () => {
      emit("generate", reportOptions);
    };

    return {
      reportOptions,
      generateReport,
    };
  },
};
</script>
