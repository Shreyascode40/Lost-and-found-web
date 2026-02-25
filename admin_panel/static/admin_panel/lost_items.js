function toggleClaims(itemId) {
    const section = document.getElementById("claims-" + itemId);

    if (section.style.display === "none") {
        section.style.display = "block";
    } else {
        section.style.display = "none";
    }
}
