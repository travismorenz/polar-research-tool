import React from "react";

const Article = ({
  authors,
  categories,
  id,
  inLibrary,
  keywords,
  onProjectPage,
  publish_date,
  summary,
  title,
  toggleInLibrary,
  url,
}) => {
  return (
    <div className="article card">
      {onProjectPage && (
        <button className="bookmark-btn" onClick={() => toggleInLibrary(id)}>
          <i className={`icon icon-bookmark ${inLibrary ? "active" : ""}`} />
        </button>
      )}
      <a href={url} target="_blank" rel="noopener noreferrer">
        <h5>{title}</h5>
      </a>
      <div id="authors">
        {authors.map((name, i) => (
          <span key={`${id}author${i}`}>
            <button className="btn-link">{name}</button>
            {i < authors.length - 1 ? ", " : ""}
          </span>
        ))}
      </div>
      <div id="keywords">
        {keywords.map((keyword, i) => (
          <span key={`${id}keyword${i}`}>
            <button className="btn-link">{keyword}</button>
              {i < keywords.length - 1 ? ", " : ""}
          </span>
        ))}
      </div>
      <div className="metadata">
        <span className="publish_date">{publish_date.slice(0, 16)}</span>
        {categories.map((name, i) => (
          <span key={`${id}category${i}`}>
            <button className="btn-link">{name}</button>
            {i < categories.length - 1 ? " | " : ""}
          </span>
        ))}
      </div>
      <p>{summary}</p>
    </div>
  );
};

export default Article;
