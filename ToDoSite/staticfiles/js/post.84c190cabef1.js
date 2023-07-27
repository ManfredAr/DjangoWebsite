function validateForm() {
        var postContent = document.getElementById("postContent").value;
        var tagContent = document.getElementById("tagContent").value;

        if (postContent.trim() === "" && tagContent.trim() === "") {
            document.getElementById("error").style.display = "block";
            return false;
        } else {
            document.getElementById("postForm").submit();
        }

    return true; 
}