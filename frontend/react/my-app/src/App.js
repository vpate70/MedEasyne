import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container } from 'react-bootstrap';
import SearchBar from './component/SearchBar.js'; 
function App() {
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = (searchQuery) => {
    console.log("Searching for:", searchQuery);
  };

  return (
    <>
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
    <h1 style={{ marginBottom: '20px' }}>
        <span style={{ color: 'red' }}>Med</span>
        <span style={{ color: 'black' }}>Easyne</span>
    </h1>
    </div>
    <Container className="mt-2">
      <SearchBar onSearch={handleSearch} />
      <div className="mt-3">
        {/* Display search results here */}
        {/* You can map through searchResults and display each result */}
      </div>
    </Container>
    </>
  );
}

export default App;
