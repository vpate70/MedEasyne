import React, { useState } from 'react';
import { Card, Button, Col, Row } from 'react-bootstrap';

const SearchResult = ({ title, summary }) => {
  const [apiResponse, setApiResponse] = useState(null);
  const [showResponse, setShowResponse] = useState(false);

  const handleButtonClick = async () => {
    if (apiResponse){
        setShowResponse(!showResponse);
    }
    else {
        try {
        const url = 'http://127.0.0.1:8000/llm';
        const options = {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: summary }),
        };
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error('Search response not OK');
        }
        const data = await response.json();
        setApiResponse(data);
        setShowResponse(true);
        } catch (error) {
        console.error('Error during search:', error);
        }
    }
  };

  return (
    <Row>
      <Col>
        <Card style={{ height: '100%' }}>
          <Card.Body>
            <Card.Title>{title}</Card.Title>
            <Card.Text>
              {summary}
            </Card.Text>
            <Button variant="primary" onClick={() => {handleButtonClick()}}>
              {showResponse ? 'Hide Details' : 'View Details'}
            </Button>
          </Card.Body>
        </Card>
      </Col>
      {apiResponse && showResponse &&
        (
          <Col>
            <Card style={{ borderRadius: '15px', height: '100%' }}>
              <Card.Body>
                <Card.Title>Text Details</Card.Title>
                <Card.Text>{apiResponse}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        )}
    </Row>
  );
};

export default SearchResult;
