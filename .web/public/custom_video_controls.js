console.log('Custom video script loaded');

// Function to initialize video controls for a given video element
function initializeVideoControls(videoElement) {
    // Assuming there's a single play/pause button and seek bar for simplicity
    const playPauseBtn = document.getElementById('playPauseBtn'); // Adjust if necessary
    const seekBar = document.getElementById('seekBar');
    
    const mainVideoPlayer = document.getElementById('video_1'); // Get the main video player by its ID
    const swapButton = document.getElementById('swap');

    const miniVideoPlayer = document.getElementById('mini_video_1');
    const miniVideoMessageContainer = document.getElementById('miniPlayerMessage');
    let lastPlayedSegmentIndex = -1; // Initialize outside timeupdate listener

    // Function to toggle play/pause
    function togglePlayPause() {
        if (videoElement.paused || videoElement.ended) {
            videoElement.play();
            playPauseBtn.textContent = 'Pause';
        } else {
            videoElement.pause();
            playPauseBtn.textContent = 'Play';
        }
    }
    videoElement.addEventListener('play', function() {
        playPauseBtn.textContent = 'Pause';
    });

    videoElement.addEventListener('pause', function() {
        playPauseBtn.textContent = 'Play';
    });

    // Update the seek bar as the video plays
    videoElement.addEventListener('timeupdate', () => {
        const currentTime = videoElement.currentTime;
        let inMarkerSegment = false;
        let markerNumber = -1; // Initialize with an invalid value

        const swapButton = document.getElementById('swap');

        // Corrected loop to use (marker, index)
        markers.forEach((marker, index) => {
            const currentTime = videoElement.currentTime;
            if (currentTime >= marker.start && currentTime <= marker.end) {
                inMarkerSegment = true;
                markerNumber = index; // Save the index of the current marker
            }
        });

        if (inMarkerSegment ) {
            // Change the video source to "segment_{index}.mp4"
            const newSource = `/segment_${markerNumber}.mp4`; // Adjust the path as needed
            if (markerNumber != lastPlayedSegmentIndex) {
                miniVideoPlayer.src = newSource;
                miniVideoPlayer.load(); // Load the new video source
                miniVideoPlayer.play(); // Optionally, start playing the mini video
                lastPlayedSegmentIndex = markerNumber;

                swapButton.disabled = false;
                swapButton.style.opacity = 1; // Make the button fully opaque when enabled
                swapButton.style.cursor = "pointer"; // Change cursor to pointer to indicate it's clickable
            }
            miniVideoMessageContainer.style.display = 'none'; // Hide the message container
        } else {
            // Display a message for inactive segment
            swapButton.disabled = true;
            swapButton.style.opacity = 0.5; // Make the button semi-transparent when disabled
            swapButton.style.cursor = "not-allowed"; // Change cursor to indicate it's not clickable
        
            miniVideoPlayer.pause(); // Optionally, pause the mini video
            miniVideoMessageContainer.textContent = 'Last Clip'; // Display your message
            miniVideoMessageContainer.style.display = 'block'; // Show the message container
            lastPlayedSegmentIndex = -1;
        }

        const value = (100 / videoElement.duration) * videoElement.currentTime;
        seekBar.value = value;
    });

    // Seek in the video when the seek bar changes
    seekBar.addEventListener('input', () => {
        const time = videoElement.duration * (seekBar.value / 100);
        videoElement.currentTime = time;
    });

    swapButton.addEventListener('click', function() {
        if (!this.disabled) {
            const segmentUrl = `/segment_${lastPlayedSegmentIndex}.mp4`; // Construct the segment URL based on the last played index
            mainVideoPlayer.src = segmentUrl; // Change the source of the main video player to the new segment
            mainVideoPlayer.load(); // Load the new source
            mainVideoPlayer.play(); // Play the new segment
        }
    });

    // Attach event listener to play/pause button
    playPauseBtn.addEventListener('click', togglePlayPause);

    // Initialize canvas for highlighting
    const highlightCanvas = document.getElementById('highlightCanvas');
    const ctx = highlightCanvas.getContext('2d');
    const markers = [{'start': 1127.62, 'end': 1161.58}, {'start': 312.18, 'end': 346.48}, {'start': 1151.24, 'end': 1183.42}, {'start': 351.1, 'end': 391.5}, {'start': 307.5, 'end': 342.14}, {'start': 256.34, 'end': 290.84}, {'start': 252.5, 'end': 287.0}, {'start': 154.38, 'end': 188.04}];

    function drawRoundedRect(ctx, x, y, width, height, radius) {
        if (width < 2 * radius) radius = width / 2;
        if (height < 2 * radius) radius = height / 2;
        ctx.beginPath();
        ctx.moveTo(x + radius, y);
        ctx.arcTo(x + width, y, x + width, y + height, radius);
        ctx.arcTo(x + width, y + height, x, y + height, radius);
        ctx.arcTo(x, y + height, x, y, radius);
        ctx.arcTo(x, y, x + width, y, radius);
        ctx.closePath();
        ctx.fill();
    }

    // Adjust canvas size and draw markers when video metadata is loaded
    videoElement.addEventListener('loadedmetadata', () => {
        // Adjust canvas size
        highlightCanvas.width = seekBar.offsetWidth;
        highlightCanvas.height = seekBar.offsetHeight;

        // Draw markers
        markers.forEach(marker => {
            const startRatio = marker.start / videoElement.duration;
            const endRatio = marker.end / videoElement.duration;
            const startX = startRatio * highlightCanvas.width;
            const width = (endRatio * highlightCanvas.width) - startX;
            const height = highlightCanvas.height; // The height of your highlight area
            const radius = 20; // The desired corner radius
        
            ctx.fillStyle = "rgba(224, 180, 164, 0.7)"; // Semi-transparent red
        
            // Call drawRoundedRect with the calculated dimensions and radius
            drawRoundedRect(ctx, startX, 0, width, height, radius);
        });        
    });


}

// MutationObserver callback to initialize controls for dynamically added videos
const callback = function(mutationsList, observer) {
    for (const mutation of mutationsList) {
        if (mutation.type === 'childList') {
            mutation.addedNodes.forEach(node => {
                // Define the specific ID you're looking for
                const specificVideoId = 'video_1'; // Replace 'specificVideoId' with the actual ID

                // Check if the added node is a video with the specific ID
                if (node.nodeName === 'VIDEO' && node.id === specificVideoId) {
                    initializeVideoControls(node);
                } else if (node.querySelector && node.querySelector(`video#${specificVideoId}`)) {
                    // If the node contains the specific video
                    const videoElement = node.querySelector(`video#${specificVideoId}`);
                    initializeVideoControls(videoElement);
                }
            });
        }
    }
};


// Create and start a MutationObserver to watch for added video elements
const observer = new MutationObserver(callback);
observer.observe(document.body, { childList: true, subtree: true });

console.log('Video controls setup observer started.');
