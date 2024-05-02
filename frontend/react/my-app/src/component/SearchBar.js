import React, { useState } from 'react';
import { Form, FormControl, Button } from 'react-bootstrap';
import SearchResult from './SearchResult'; 

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const url = 'http://127.0.0.1:8000/search';
      const queryValue = query.toLowerCase();
      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: queryValue }),
      };
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error('Search response not OK');
      }
      const data = await response.json();
      const { titles, authors, abstracts } = data;
      const searchResults = titles.map((title, index) => ({
        id: index, 
        title,
        summary: abstracts[index],
        authors: authors[index]
      }));
      setResults(searchResults);
    } catch (error) {
      console.error('Error during search:', error);
    }
  };

  return (
    <div style={{  marginTop: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Form inline>
          <FormControl
            type="text"
            placeholder="Search"
            style={{ width: '400px', marginRight: '10px' }}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </Form>
        <Button variant="outline-success" onClick={handleSearch}>Search</Button>
      </div>
      <div style={{ marginTop: '20px' }}>
        {results.map(result => (
              <SearchResult
                title={result.title}
                summary={result.summary}
                authors={result.authors}
              />
        ))}
      </div>
    </div>
  );
};

export default SearchBar;
