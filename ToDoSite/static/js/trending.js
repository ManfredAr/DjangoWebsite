function validateForm() {
    var search = document.getElementById("query").value;

    if (search.trim() === "") {
        document.getElementById("form-error").style.display = "block";
        return false;
    } else {
        document.getElementById("postForm").submit();
    }

    return true; 
}