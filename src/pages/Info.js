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
      <header>
        <h1>{title}</h1>
      </header>
      <form onSubmit={handleSubmit}>
        <input
          list={title}
          type="text"
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
        <button type="submit">Submit</button>
      </form>
      {items.map((item, index) => (
        <div key={index}>
          {item}
          <button onClick={() => handleDelete(index)}>X</button>
        </div>
      ))}
    </div>
  );
}

export default Info;