// Add event listener to the GIF button
const gifButton = document.getElementById('gif-button');
gifButton.addEventListener('click', toggleGifWindow);

// Function to toggle the GIF window
function toggleGifWindow() {
  const gifWindow = document.getElementById('gif-window');
  gifWindow.style.display = gifWindow.style.display === 'block' ? 'none' : 'block';

  // Load GIFs from an external source
  if (gifWindow.style.display === 'block') {
    loadGifs();
  }
}

// Function to load GIFs
function loadGifs() {
  // Make an API call or fetch GIFs from a data source
}