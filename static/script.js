document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const apiKeyScreen = document.getElementById('api-key-screen');
    const storyCreatorScreen = document.getElementById('story-creator-screen');
    const saveApiKeysButton = document.getElementById('save-api-keys');
    const generateStoryButton = document.getElementById('generate-story');
    const storyDisplay = document.getElementById('story-display');
    const storyControls = document.getElementById('story-controls');
    const readAloudButton = document.getElementById('read-aloud');
    const downloadPdfButton = document.getElementById('download-pdf');

    // Global variable to hold the generated story data
    let storyData = {};

    // --- API Key Management ---

    // Check if API key is already in localStorage and show the appropriate screen
    if (localStorage.getItem('openai_api_key')) {
        apiKeyScreen.style.display = 'none';
        storyCreatorScreen.style.display = 'block';
    }

    // Save the OpenAI API key to localStorage
    saveApiKeysButton.addEventListener('click', () => {
        const openAIKey = document.getElementById('openai-api-key').value;
        if (openAIKey) {
            localStorage.setItem('openai_api_key', openAIKey);
            apiKeyScreen.style.display = 'none';
            storyCreatorScreen.style.display = 'block';
        } else {
            alert('Please enter your OpenAI API key.');
        }
    });

    // --- Story Generation ---

    // Handle the "Generate Story" button click
    generateStoryButton.addEventListener('click', async () => {
        // Get form values
        const title = document.getElementById('story-title').value;
        const age = document.getElementById('story-age').value;
        const tone = document.getElementById('story-tone').value;
        const language = document.getElementById('story-language').value;
        const openAIKey = localStorage.getItem('openai_api_key');

        if (!title || !age || !tone || !language) {
            alert('Please fill out all fields.');
            return;
        }

        // Show a loading message
        storyDisplay.innerHTML = '<p>Generating story... Please wait.</p>';

        // Fetch the story from the backend
        const response = await fetch('/generate-story', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, age, tone, language, openai_api_key: openAIKey })
        });

        storyData = await response.json();
        storyData.title = title;

        // --- Display Story and Pagination ---

        // Create the story display elements
        storyDisplay.innerHTML = `
            <h2 id="story-title-display"></h2>
            <img id="story-image-display" src="" alt="Generated story image" style="width:100%; display:none;">
            <div id="paginated-story"></div>
            <div id="pagination-controls" style="display: none; justify-content: space-between; margin-top: 1rem;">
                <button id="prev-page">Previous</button>
                <span id="page-indicator"></span>
                <button id="next-page">Next</button>
            </div>
        `;

        // Get the newly created elements
        const storyTitleDisplay = document.getElementById('story-title-display');
        const storyImageDisplay = document.getElementById('story-image-display');
        const paginatedStory = document.getElementById('paginated-story');
        const paginationControls = document.getElementById('pagination-controls');
        const pageIndicator = document.getElementById('page-indicator');
        const prevPageButton = document.getElementById('prev-page');
        const nextPageButton = document.getElementById('next-page');

        // Populate the story display
        storyTitleDisplay.textContent = title;
        storyImageDisplay.src = storyData.image_url;
        storyImageDisplay.style.display = 'block';

        const storyPages = storyData.story_text.split('\n\n').filter(p => p.trim() !== '');
        let currentPage = 0;

        function displayPage(pageIndex) {
            paginatedStory.innerHTML = `<p>${storyPages[pageIndex]}</p>`;
            pageIndicator.textContent = `Page ${pageIndex + 1} of ${storyPages.length}`;
        }

        displayPage(currentPage);

        paginationControls.style.display = 'flex';
        storyControls.style.display = 'flex';

        // Pagination controls event listeners
        prevPageButton.addEventListener('click', () => {
            if (currentPage > 0) {
                currentPage--;
                displayPage(currentPage);
            }
        });

        nextPageButton.addEventListener('click', () => {
            if (currentPage < storyPages.length - 1) {
                currentPage++;
                displayPage(currentPage);
            }
        });
    });

    // --- Story Controls ---

    // "Read Aloud" button
    readAloudButton.addEventListener('click', () => {
        const storyText = document.getElementById('paginated-story').textContent;
        const utterance = new SpeechSynthesisUtterance(storyText);
        speechSynthesis.speak(utterance);
    });

    // "Download PDF" button
    downloadPdfButton.addEventListener('click', () => {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        const title = storyData.title;
        doc.text(title, 10, 10);

        const storyPages = storyData.story_text.split('\n\n').filter(p => p.trim() !== '');
        let y = 20;
        storyPages.forEach(page => {
            const lines = doc.splitTextToSize(page, 180);
            if (y + (lines.length * 7) > 280) {
                doc.addPage();
                y = 10;
            }
            doc.text(lines, 10, y);
            y += (lines.length * 7) + 5;
        });

        doc.save(`${title.replace(/\s+/g, '_')}.pdf`);
    });
});
