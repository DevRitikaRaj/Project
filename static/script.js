// Global variables
let viewer3d = null;
let currentMolecule = null;
let currentStyle = 'stick';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadExamples();
    initializeEventListeners();
    showSection('hero'); // Show hero section by default
});

// Event listeners
function initializeEventListeners() {
    // SMILES input enter key
    const smilesInput = document.getElementById('smiles-input');
    if (smilesInput) {
        smilesInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                analyzeMolecule();
            }
        });
    }
}

// Navigation function
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section, .hero');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    
    // Show the requested section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.style.display = 'block';
        
        // Special handling for examples section
        if (sectionId === 'examples') {
            loadExamples();
        }
    }
}

// Main analysis function
async function analyzeMolecule() {
    const smilesInput = document.getElementById('smiles-input');
    const smiles = smilesInput.value.trim();
    
    if (!smiles) {
        showError('Please enter a SMILES string');
        return;
    }
    
    showLoading(true);
    hideError();
    hideResults();
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ smiles: smiles })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        if (data.success) {
            currentMolecule = data;
            displayResults(data);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

// Display analysis results
function displayResults(data) {
    // Display 2D structure
    display2DStructure(data.structure_2d);
    
    // Display 3D structure
    display3DStructure(data.structure_3d);
    
    // Display properties
    displayProperties(data.properties);
    
    // Display analysis results
    displayAnalysis(data.properties);
    
    // Show results section
    showResults();
}

// Display 2D molecular structure
function display2DStructure(imageData) {
    const container = document.getElementById('structure-2d');
    if (imageData) {
        container.innerHTML = `<img src="${imageData}" alt="2D Molecular Structure" />`;
    } else {
        container.innerHTML = '<p>2D structure not available</p>';
    }
}

// Display 3D molecular structure
function display3DStructure(structure3d) {
    const container = document.getElementById('structure-3d');
    
    if (!structure3d || structure3d.error) {
        container.innerHTML = '<p>3D structure not available</p>';
        return;
    }
    
    // Clear previous content
    container.innerHTML = '';
    
    // Initialize 3Dmol.js viewer
    viewer3d = $3Dmol.createViewer(container, {
        defaultcolors: $3Dmol.rasmolElementColors
    });
    
    // Create molecule data in SDF format
    const sdfData = createSDFFromStructure(structure3d);
    
    // Add molecule to viewer
    viewer3d.addModel(sdfData, 'sdf');
    
    // Set initial style
    setMoleculeStyle(currentStyle);
    
    // Render
    viewer3d.zoomTo();
    viewer3d.render();
}

// Create SDF format from structure data
function createSDFFromStructure(structure) {
    const atoms = structure.atoms;
    const bonds = structure.bonds;
    
    if (!atoms || atoms.length === 0) {
        return '';
    }
    
    // Build SDF format
    let sdf = `
  3Dmol.js    

${atoms.length.toString().padStart(3)}${bonds.length.toString().padStart(3)}  0  0  0  0  0  0  0  0999 V2000
`;
    
    // Add atoms
    atoms.forEach(atom => {
        const x = atom.x.toFixed(4).padStart(10);
        const y = atom.y.toFixed(4).padStart(10);
        const z = atom.z.toFixed(4).padStart(10);
        const element = atom.element.padEnd(3);
        sdf += `${x}${y}${z} ${element} 0  0  0  0  0  0  0  0  0  0  0  0\n`;
    });
    
    // Add bonds
    bonds.forEach(bond => {
        const atom1 = (bond.atom1 + 1).toString().padStart(3);
        const atom2 = (bond.atom2 + 1).toString().padStart(3);
        let bondOrder = '1';
        
        if (bond.bondType === 'DOUBLE') bondOrder = '2';
        else if (bond.bondType === 'TRIPLE') bondOrder = '3';
        else if (bond.bondType === 'AROMATIC') bondOrder = '4';
        
        sdf += `${atom1}${atom2}  ${bondOrder}  0  0  0  0\n`;
    });
    
    sdf += 'M  END\n$$$$\n';
    
    return sdf;
}

// Set 3D molecule visualization style
function setMoleculeStyle(style) {
    if (!viewer3d) return;
    
    viewer3d.removeAllModels();
    
    if (currentMolecule && currentMolecule.structure_3d) {
        const sdfData = createSDFFromStructure(currentMolecule.structure_3d);
        viewer3d.addModel(sdfData, 'sdf');
        
        switch (style) {
            case 'stick':
                viewer3d.setStyle({}, {stick: {radius: 0.15}});
                break;
            case 'sphere':
                viewer3d.setStyle({}, {sphere: {scale: 0.3}, stick: {radius: 0.1}});
                break;
            case 'cartoon':
                viewer3d.setStyle({}, {cartoon: {color: 'spectrum'}});
                break;
            case 'line':
                viewer3d.setStyle({}, {line: {}});
                break;
            default:
                viewer3d.setStyle({}, {stick: {radius: 0.15}});
        }
        
        viewer3d.render();
    }
}

// Display molecular properties
function displayProperties(properties) {
    const container = document.getElementById('properties');
    
    const propertyItems = [
        { label: 'Molecular Formula', value: properties.molecular_formula || 'N/A' },
        { label: 'Molecular Weight', value: properties.molecular_weight ? `${properties.molecular_weight.toFixed(2)} g/mol` : 'N/A' },
        { label: 'LogP', value: properties.logp ? properties.logp.toFixed(2) : 'N/A' },
        { label: 'TPSA', value: properties.tpsa ? `${properties.tpsa.toFixed(2)} Ų` : 'N/A' },
        { label: 'H-Bond Donors', value: properties.hbd_count || 0 },
        { label: 'H-Bond Acceptors', value: properties.hba_count || 0 },
        { label: 'Rotatable Bonds', value: properties.rotatable_bonds || 0 },
        { label: 'Aromatic Rings', value: properties.aromatic_rings || 0 }
    ];
    
    container.innerHTML = propertyItems.map(item => `
        <div class="property-item">
            <div class="property-value">${item.value}</div>
            <div class="property-label">${item.label}</div>
        </div>
    `).join('');
}

// Display AI analysis results
function displayAnalysis(properties) {
    const container = document.getElementById('analysis');
    
    const getRiskClass = (risk) => {
        switch (risk) {
            case 'Low Risk': return 'risk-low';
            case 'Medium Risk': return 'risk-medium';
            case 'High Risk': return 'risk-high';
            default: return '';
        }
    };
    
    const getDrugLikenessClass = (score) => {
        if (score >= 0.8) return 'risk-low';
        if (score >= 0.5) return 'risk-medium';
        return 'risk-high';
    };
    
    const analysisItems = [
        {
            label: 'Lipinski Violations',
            value: `${properties.lipinski_violations || 0}/4`,
            class: (properties.lipinski_violations || 0) <= 1 ? 'risk-low' : 'risk-high'
        },
        {
            label: 'Drug-likeness Score',
            value: properties.drug_likeness_score ? `${(properties.drug_likeness_score * 100).toFixed(1)}%` : 'N/A',
            class: getDrugLikenessClass(properties.drug_likeness_score || 0)
        },
        {
            label: 'Toxicity Prediction',
            value: properties.toxicity_prediction || 'Unknown',
            class: getRiskClass(properties.toxicity_prediction)
        }
    ];
    
    container.innerHTML = analysisItems.map(item => `
        <div class="analysis-item">
            <span class="analysis-label">${item.label}</span>
            <span class="analysis-value ${item.class}">${item.value}</span>
        </div>
    `).join('');
}

// 3D Visualization controls
function resetView() {
    if (viewer3d) {
        viewer3d.zoomTo();
        viewer3d.render();
    }
}

function toggleStyle() {
    const styles = ['stick', 'sphere', 'line', 'cartoon'];
    const currentIndex = styles.indexOf(currentStyle);
    currentStyle = styles[(currentIndex + 1) % styles.length];
    setMoleculeStyle(currentStyle);
}

// Load example molecules
async function loadExamples() {
    try {
        const response = await fetch('/api/examples');
        const examples = await response.json();
        displayExamples(examples);
    } catch (error) {
        console.error('Error loading examples:', error);
    }
}

// Display example molecules
function displayExamples(examples) {
    const container = document.getElementById('examples-grid');
    
    container.innerHTML = examples.map(example => `
        <div class="example-card" onclick="analyzeExample('${example.smiles}')">
            <div class="example-name">${example.name}</div>
            <div class="example-smiles">${example.smiles}</div>
            <div class="example-description">${example.description}</div>
        </div>
    `).join('');
}

// Analyze example molecule
function analyzeExample(smiles) {
    const smilesInput = document.getElementById('smiles-input');
    smilesInput.value = smiles;
    showSection('analyzer');
    analyzeMolecule();
}

// UI helper functions
function showLoading(show) {
    const loading = document.getElementById('loading');
    loading.style.display = show ? 'block' : 'none';
}

function showResults() {
    const results = document.getElementById('results');
    results.style.display = 'block';
}

function hideResults() {
    const results = document.getElementById('results');
    results.style.display = 'none';
}

function showError(message) {
    const error = document.getElementById('error');
    error.textContent = message;
    error.style.display = 'block';
}

function hideError() {
    const error = document.getElementById('error');
    error.style.display = 'none';
}

// Search functionality
async function searchMolecules() {
    const query = document.getElementById('search-input').value.trim();
    
    if (!query) {
        return;
    }
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        const results = await response.json();
        displaySearchResults(results);
        
    } catch (error) {
        console.error('Search error:', error);
    }
}

function displaySearchResults(results) {
    // Implementation for search results display
    console.log('Search results:', results);
}

// Utility functions
function formatNumber(num, decimals = 2) {
    if (typeof num !== 'number') return 'N/A';
    return num.toFixed(decimals);
}

function downloadResults() {
    if (!currentMolecule) {
        alert('No molecule data to download');
        return;
    }
    
    const data = {
        smiles: currentMolecule.smiles,
        properties: currentMolecule.properties,
        timestamp: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `molecule_analysis_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Animation for hero section molecule
function animateHeroMolecule() {
    const molecule = document.querySelector('.molecule-animation');
    if (molecule) {
        // Add some CSS animation or canvas-based animation here
        molecule.style.animation = 'float 6s ease-in-out infinite';
    }
}

// Initialize hero animation
document.addEventListener('DOMContentLoaded', function() {
    animateHeroMolecule();
});

// Export functions for global access
window.showSection = showSection;
window.analyzeMolecule = analyzeMolecule;
window.analyzeExample = analyzeExample;
window.resetView = resetView;
window.toggleStyle = toggleStyle;
window.downloadResults = downloadResults;
  