function changeTab(tabID, tabName) {
    var i, tabContent, tabButton;

    // Hide all tab content
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }

    // Get all tab buttons and remove "active"
    tabButton = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabButton.length; i++) {
        tabButton[i].classList.remove("active");
    }

    // Show current tab, add "active" to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabID).classList.add("active");
}

function clickFollow(buttonID) {
    document.getElementById(buttonID).innerHTML = "Unfollow";
    const follow = document.querySelector('.follow');
    if (document.getElementById(buttonID).classList.contains("clicked")) {
        document.getElementById(buttonID).innerHTML = "Follow";
        follow.style.backgroundColor = "#808080";
        follow.style.color = "black";
    }
    else {
        document.getElementById(buttonID).innerHTML = "Unfollow";
        follow.style.backgroundColor = "#ffcc00";
    }
    document.getElementById(buttonID).classList.toggle("clicked")
}

// Button more options-more
const buttonMore = document.querySelector('.button.more');
const optionsWindow = document.querySelector('.options-window');

buttonMore.addEventListener('click', () => {
optionsWindow.classList.toggle('show');
});
// 

// Tweet input
const twt = document.querySelector('.twt');
const messageWindow = document.querySelector('.message-window');
const page = document.querySelector('.page');
var post_id = document.getElementById('post_id_input');

var element;

twt.addEventListener('click', () => {
    messageWindow.classList.toggle('show');
    post_id.value = null;
});

function clickReaction(reactID) {
    let tag = String(reactID);

    if (tag.includes('Reply')){
        document.getElementById(reactID).classList.toggle("clicked");
        messageWindow.classList.toggle('show');
        page.scrollTo({ top: 0, behavior: 'smooth' });
        element = document.getElementById(reactID);
        post_id.value = element.dataset.value;
    }
    else if (tag.includes('Like')){
        document.getElementById(reactID).classList.toggle("clicked");
        document.getElementById(reactID).submit();
        
    }
    
}


function sendMessage() {
    // Get the text input value
    var tweet = $('.editable').html();

    // Get the uploaded image (if any)
    var image = $('#fileInput').prop('files')[0];

    // Get the CSRF token value
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    // Create a FormData object to send the data
    var formData = new FormData();
    formData.append('post_id', post_id.value);
    formData.append('tweet', tweet);
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('name', twt); 
    if (image) {
    formData.append('image', image);
    }
    console.log(post_id);
    // Send the data using Ajax
    $.ajax({
        url: '', 
        type: 'POST',
        data: formData,

        success: function(response) {
            // Handle the success response
            console.log(alert);
        },
        error: function(xhr, status, error) {
            // Handle the error response
            console.error(error);
        }
    });

    // Close the message window
    messageWindow.classList.remove('show');
    // Clear the textarea
    editableInput.innerHTML = null;
    counter.innerHTML = '200';
    input.value = "";
    
}

// Bare bones at the moment.
function handleFileUpload(event) {
    const file = event.target.files[0];

    // Check if a file is selected
    if (file) {
    // Check the file type
        if (file.type.startsWith('image/') || file.type.startsWith('video/')) {
        
        const maxSizeInBytes = 10 * 1024 * 1024; // 10MB
        if (file.size <= maxSizeInBytes) {
            // File is valid, perform further actions
            console.log('File is valid:', file);
            // You can process the file or display a preview here
        } else {
            // File size is too large
            console.log('File size exceeds the maximum limit.');
            // Display an error message or take appropriate action
            event.target.value = null;
        }
        } else {
            // Invalid file type
            console.log('Invalid file type.');
            // Display an error message or take appropriate action
            event.target.value = null;
    }
    }
}
