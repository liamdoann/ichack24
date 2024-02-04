import React, { useState } from 'react';

function Info({ title, text, setText, items, setItems, quotes }) {

  const handleSubmit = (e) => {
    e.preventDefault();
    setItems([...items, text]);
    setText('');
  };

  const handleDelete = (index) => {
    const newItems = [...items];
    newItems.splice(index, 1);
    setItems(newItems);
  };

  return (
    <div>
      <h3>{title}</h3>
      <form onSubmit={handleSubmit}>
        <input
          list={title}
          type="text"
          className="input-form"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <datalist id={title}>
          {quotes.map((order, index) => (
            <option key={index} value={order}>
              {order}
            </option>
          ))}
        </datalist>
        <button className="submitItem"type="submit">→</button>
      </form>
      {items.map((item, index) => (
        <div className="element" key={index}>
          <span>{item}</span>
          <button className="delete-button" onClick={() => handleDelete(index)}>X</button>
        </div>
      ))}
    </div>
  );
}

export default Info;