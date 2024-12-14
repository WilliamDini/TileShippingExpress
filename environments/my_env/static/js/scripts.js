let selectedIDs = [];
var output = '';
let addedContainers = [];
let string = "";

function changeBackgroundColor(itemID) {
    let element = document.getElementById(itemID).style.background;
    let stringArray = itemID.split("_");
    let id = stringArray[0];
    let name = stringArray[1];
    if (element == "white" && name != "UNUSED") {
        document.getElementById(itemID).style.background = "rgb(114, 231, 146)";
        checkSelectedIDs(itemID, 0);
    } else if (document.getElementById(itemID).style.background == "rgb(114, 231, 146)") {
        document.getElementById(itemID).style.background = "white";
        checkSelectedIDs(itemID, 1);
    }
}

function checkSelectedIDs(itemID, action) {
    if (action == 0) {
        selectedIDs.push(itemID);
    } else {
        for (let i = 0; i < selectedIDs.length; i++) {
            if (selectedIDs[i] == itemID) {
                selectedIDs.splice(i, 1);
            }
        }
    }
    displayArray();
}

function displayArray() {
    //alert("in displayArray");
    if (selectedIDs.length == 0) {
        output = '<p>Selected Containers:</p>';
    } else {
        output = '<p>Selected Containers:</p>';
        for (var i = 0; i < selectedIDs.length; i++) {
            let stringArray = selectedIDs[i].split("_");
            output += '<p>' + stringArray[1] + '</p>';
        }
    }
    document.getElementById("arrayContainer").innerHTML = output;
}

function changeShipArray() {
    //alert("in changeShipArray");
    fetch('/Transfer-process-changes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(selectedIDs)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status == "success") {
                alert("array processed successfully: " + data.array);
            } else {
                alert("Null Array processed successfully: " + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
}

function handleSubmittedContainer() {
    let inputName = document.getElementById('containerName').value;
    let inputWeight = parseInt(document.getElementById('containerWeight').value);
    alert(inputWeight);

    if (Number.isInteger(inputWeight) && inputWeight >= 0 && inputWeight < 100000 && inputName != "") {
        data = {
            containerName: inputName,
            containerWeight: inputWeight
        };
        addedContainers.push(data);
        string += addedContainers[addedContainers.length - 1].containerName + " ";
        alert("added containers: " + string);
    } else {
        alert("Invalid input, please try again.");
    }
}

if (window.location.pathname == "/Transfer-comingoff") {
    window.onload = displayArray;
}

function handleCommentInput() {
    const comment = document.getElementById('comment').value;
    //alert(comment)
    if (!comment.trim()) {
        alert("Please enter a comment.");
        return;
    }


    fetch('/log_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ comment: comment }),
    })
    .then(response => {
        if (response.ok) {
            document.getElementById('comment').value = '';
            const feedback = document.getElementById('comment-feedback');
            feedback.style.display = 'block';
            setTimeout(() => feedback.style.display = 'none', 3000);
        } else {
            alert("Failed to log the comment. Please try again.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
}