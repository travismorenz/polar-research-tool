import React, { useState, useRef } from "react";

const Project = ({
  addKeyphrase,
  removeKeyphrase,
  addCategory,
  removeCategory,
  leaveProject,
  id,
  name,
  keyphrases,
  categories,
}) => {
  const [newKeyphrase, setNewKeyphrase] = useState("");
  const [newCategory, setNewCategory] = useState("");
  const keyphraseBottom = useRef();
  const categoryBottom = useRef();

  if (id === "_default") return null;
  return (
    <div className="project card">
      <h5>{name}</h5>
      <div className="card-body">
        <div className="card-content">
          <h6>Keyphrases</h6>
          <ul className="max-height-list">
            {keyphrases.map((k) => (
              <li key={k}>
                {k}
                <button
                  className="remove"
                  onClick={() => removeKeyphrase(k, id)}
                >
                  X
                </button>
              </li>
            ))}
            <div ref={keyphraseBottom} />
          </ul>
          <input
            value={newKeyphrase}
            onChange={(e) => setNewKeyphrase(e.target.value)}
          />
          <button
            onClick={async () => {
              await addKeyphrase(newKeyphrase, id);
              setNewKeyphrase("");
              keyphraseBottom.current.scrollIntoView();
            }}
          >
            Add
          </button>
        </div>
        <div className="card-content">
          <h6>Categories</h6>
          <ul className="max-height-list">
            {categories.map((c) => (
              <li key={c}>
                {c}
                <button
                  className="remove"
                  onClick={() => removeCategory(c, id)}
                >
                  X
                </button>
              </li>
            ))}
            <div ref={categoryBottom} />
          </ul>
          <input
            value={newCategory}
            onChange={(e) => setNewCategory(e.target.value)}
          />
          <button
            onClick={async () => {
              await addCategory(newCategory, id);
              setNewCategory("");
              categoryBottom.current.scrollIntoView();
            }}
          >
            Add
          </button>
        </div>
      </div>
      <div className="card-footer">
        <button
          className="btn leave"
          onClick={() => leaveProject({ name, id })}
        >
          Leave Project
        </button>
      </div>
    </div>
  );
};

export default Project;
