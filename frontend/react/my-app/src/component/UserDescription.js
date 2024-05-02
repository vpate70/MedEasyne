import React, { useState } from 'react';
import { Form, FormControl } from 'react-bootstrap';

const UserDescription = () => {
  const [description, setDescription] = useState('');

  return (
    <div style={{  marginTop: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'left', justifyContent: 'center' }}>
        <Form inline>
            <FormControl
                placeholder="I am a [middle school student | medical student | licensed doctor]"
                style={{ width: '500px', height: '80px' }}
                as="textarea" // This renders a multiline textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            </Form>
      </div>
    </div>
  );
};

export default UserDescription;
