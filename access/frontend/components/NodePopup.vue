<template>
  <div v-if="visible" class="popup-overlay" @click="closePopup">
    <div class="popup-content" @click.stop>
      <div class="popup-header">
        <h5 class="popup-title">{{ nodeData?.label || 'Node Information' }}</h5>
        <button type="button" class="popup-close" @click="closePopup">&times;</button>
      </div>
      <div class="popup-body">
        <div v-if="nodeData">
          <div class="popup-row">
            <div class="popup-col">
              <strong>ID:</strong> {{ nodeData.id }}
            </div>
            <div class="popup-col">
              <strong>Label:</strong> {{ nodeData.label }}
            </div>
          </div>
          <div class="popup-row" v-if="nodeData.color">
            <div class="popup-col">
              <strong>Color:</strong> 
              <span class="color-badge" :style="{ backgroundColor: nodeData.color }">
                {{ nodeData.color }}
              </span>
            </div>
          </div>
          <div class="popup-row" v-if="nodeData.group">
            <div class="popup-col">
              <strong>Group:</strong> {{ nodeData.group }}
            </div>
          </div>
          <div class="popup-row" v-if="nodeData.description">
            <div class="popup-col-full">
              <strong>Description:</strong>
              <p class="description">{{ nodeData.description }}</p>
            </div>
          </div>
          <div class="popup-row" v-if="nodeData.properties">
            <div class="popup-col-full">
              <strong>Properties:</strong>
              <pre class="properties">{{ JSON.stringify(nodeData.properties, null, 2) }}</pre>
            </div>
          </div>
        </div>
        <div v-else>
          <p class="text-muted">No node data available.</p>
        </div>
      </div>
      <div class="popup-footer">
        <button type="button" class="popup-btn" @click="closePopup">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  nodeData: {
    type: Object,
    default: null
  },
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const closePopup = () => {
  emit('close')
}

// Method to show the popup
const showPopup = () => {
  emit('show')
}

// Expose methods to parent component
defineExpose({
  showPopup
})
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #dee2e6;
}

.popup-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.popup-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.popup-close:hover {
  color: #000;
}

.popup-body {
  padding: 20px;
}

.popup-row {
  display: flex;
  margin-bottom: 10px;
  gap: 15px;
}

.popup-col {
  flex: 1;
}

.popup-col-full {
  width: 100%;
}

.color-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  color: white;
  font-size: 0.8rem;
  margin-left: 5px;
}

.description {
  margin: 5px 0 0 0;
  color: #666;
}

.properties {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  margin: 5px 0 0 0;
  overflow-x: auto;
}

.popup-footer {
  padding: 15px 20px;
  border-top: 1px solid #dee2e6;
  text-align: right;
}

.popup-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.popup-btn:hover {
  background-color: #5a6268;
}

.text-muted {
  color: #6c757d;
  font-style: italic;
}
</style> 