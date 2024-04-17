  function search() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    const results = ["result1", "result2", "result3"];
    displayResults(results);
  }
  
  function displayResults(results) {
    const searchResults = document.getElementById("searchResults");
    searchResults.innerHTML = "";
    if (results.length === 0) {
      searchResults.innerHTML = "<li>No results found.</li>";
    } else {
      results.forEach(result => {
        const li = document.createElement("li");
        li.innerHTML = `<p>${result}</p>`;
        searchResults.appendChild(li);
      });
    }
  }
  