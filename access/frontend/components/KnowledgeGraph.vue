<template>
  <div class="knowledge-graph-container">
    <div class="zoom-controls">
      <button @click="zoomIn" class="zoom-btn zoom-in">
        <span>+</span>
      </button>
      <button @click="zoomOut" class="zoom-btn zoom-out">
        <span>−</span>
      </button>
      <button @click="resetZoom" class="zoom-btn zoom-reset">
        <span>⟲</span>
      </button>
    </div>
    <div id="network" style="width: 100%; height: 600px; border: 1px solid #ccc; background: #0d0d0d;"></div>
    <NodePopup 
      :nodeData="selectedNode" 
      :visible="showPopup"
      @close="closePopup" 
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import * as vis from 'vis-network/standalone'
import NodePopup from './NodePopup.vue'

const selectedNode = ref(null)
const showPopup = ref(false)
const network = ref(null)

// Color map for node types
const nodeColors = {
  article: '#f719e9', // blue
  keyword: '#dabbf2', // green
  source: '#f5f2f7',  // red
  default: '#AAAAAA'  // gray fallback
}

// Color map for edge types (relation types)
const edgeColors = {
  published: '#FF851B', // orange for 'PUBLISHED'
  default: '#4037c4'
}

// Custom hardcoded knowledge graph data
const nodes = [
  { id: 1, label: 'article', description: 'A human being or individual', properties: { type: 'entity', category: 'human' } },
  { id: 2, label: 'keyword', description: 'A large human settlement', properties: { type: 'location', category: 'urban' } },
  { id: 3, label: 'source', description: 'A sovereign state or nation', properties: { type: 'location', category: 'national' } },
  { id: 4, label: 'article', description: 'A business organization', properties: { type: 'organization', category: 'business' } },
  { id: 5, label: 'keyword', description: 'An educational institution', properties: { type: 'organization', category: 'education' } }
]

const edges = [
  { source: 1, target: 2, type: 'PUBLISHED' },
  { source: 2, target: 3, type: 'PUBLISHED' },
  { source: 1, target: 4, type: 'PUBLISHED' },
  { source: 1, target: 5, type: 'PUBLISHED' }
]

const closePopup = () => {
  showPopup.value = false
  selectedNode.value = null
}

const zoomIn = () => {
  if (network.value) {
    const scale = network.value.getScale()
    network.value.moveTo({ scale: scale * 1.2 })
  }
}

const zoomOut = () => {
  if (network.value) {
    const scale = network.value.getScale()
    network.value.moveTo({ scale: scale * 0.8 })
  }
}

const resetZoom = () => {
  if (network.value) {
    network.value.fit()
  }
}

onMounted(async () => {
  let graphData
  try {
    const res = await axios.get('http://localhost:8001/graph_data')
    graphData = res.data
    console.log('API data received:', graphData)
  } catch (error) {
    console.warn('API not available, using hardcoded data:', error.message)
    graphData = { nodes, edges }
  }

  // Assign colors based on label for nodes
  const coloredNodes = graphData.nodes.map(node => ({
    ...node,
    color: nodeColors[node.label?.toLowerCase()] || nodeColors.default
  }))

  // Map edge properties for vis-network and assign colors
  const coloredEdges = graphData.edges.map(edge => ({
    ...edge,
    from: edge.from ?? edge.source,
    to: edge.to ?? edge.target,
    label: edge.label ?? edge.type,
    color: edgeColors[(edge.label ?? edge.type)?.toLowerCase()] || edgeColors.default
  }))

  const container = document.getElementById('network')
  const data = {
    nodes: new vis.DataSet(coloredNodes),
    edges: new vis.DataSet(coloredEdges)
  }
  const options = {
    nodes: { shape: 'dot', size: 20, font: { color: '#fff' } },
    edges: { font: { size: 12, color: 'black' }, arrows: 'to' },
    physics: { enabled: true, solver: 'barnesHut' },
    interaction: { hover: true, zoomView: true, dragView: true }
  }
  
  network.value = new vis.Network(container, data, options)
  
  // Handle node clicks
  network.value.on('click', function(params) {
    if (params.nodes.length > 0) {
      const nodeId = params.nodes[0]
      const nodeData = data.nodes.get(nodeId)
      selectedNode.value = nodeData
      showPopup.value = true
      console.log('Clicked on node:', nodeData)
    }
  })
})
</script>

<style scoped>
.knowledge-graph-container {
  position: relative;
}

.zoom-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.zoom-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.zoom-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.zoom-btn:active {
  transform: scale(0.95);
}

.zoom-in {
  background: rgba(73, 17, 102, 0.9);
  color: white;
}

.zoom-out {
  background: rgba(174, 91, 229, 0.9);
  color: white;
}

.zoom-reset {
  background: rgba(255, 255, 255, 0.9);
  color: white;
}

#network {
  width: 100%;
  height: 600px;
  border: 1px solid #ccc;
  border-radius: 20px;
  background: #26023b;
}
</style>
  