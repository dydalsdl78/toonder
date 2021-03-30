import React from 'react';
import Preview from './Preview';

function SearchPreview(props) {
  return (
    <div>
      {props.map((preview) => {
          <Preview key={preview.id} preview={preview}/>
      })}
    </div>
  );
}

export default SearchPreview;