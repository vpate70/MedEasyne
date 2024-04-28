  async function search() {
    const url = 'http://127.0.0.1:8000/search';
    const query = document.getElementById("searchInput").value.toLowerCase();
    options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({query: query}),
    };
    const response = await fetch(url, options);
    if (!response.ok) {
        throw new Error('Search response not OK');
    }
    const results = await response.json();
    // note we have results.abstracts that we can then feed to the llm as needed.
    // the lists are parallel: results.titles[i] corresponds to results.abstracts[i]
    displayResults(results.titles);
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
  