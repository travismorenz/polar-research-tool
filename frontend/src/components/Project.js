import React, { useState } from "react";

const Project = ({ addKeyphrase, id, name, keyphrases, categories }) => {
  const [newKeyphrase, setNewKeyphrase] = useState("");
  const [newCategory, setNewCategory] = useState("");

  if (id === "_default") return null;
  return (
    <div className="project card">
      <h5>{name}</h5>
      <div className="card-body">
        <div className="card-content">
          <h6>Keyphrases</h6>
          <ul className="max-height-list">
            {keyphrases.map((k) => (
              <li key={k}>{k}</li>
            ))}
          </ul>
          <input
            value={newKeyphrase}
            onChange={(e) => setNewKeyphrase(e.target.value)}
          />
          <button
            onClick={() => {
              addKeyphrase(newKeyphrase, id);
              setNewKeyphrase("");
            }}
          >
            +
          </button>
        </div>
        <div className="card-content">
          <h6>Categories</h6>
          <ul className="max-height-list">
            {categories.map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>
          <input
            value={newCategory}
            onChange={(e) => setNewCategory(e.target.value)}
          />
          <button>+</button>
        </div>
      </div>
      <div className="card-footer">
        <button className="btn leave">Leave Project</button>
      </div>
    </div>
  );
};

export default Project;
