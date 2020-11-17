import React from "react";

const Article = ({
  authors,
  categories,
  id,
  publish_date,
  summary,
  title,
  isViewingProject,
  tab,
  changeArticleTab,
  url,
}) => {
  return (
    <div className="article card">
      <a href={url} target="_blank" rel="noopener noreferrer">
        <h5>{title}</h5>
      </a>
      <div id="authors">
        {authors.map((name, i) => (
          <span key={`${id}author${i}`}>
            {name}
            {i < authors.length - 1 ? ", " : ""}
          </span>
        ))}
      </div>
      <div className="metadata">
        <span className="publish_date">{publish_date.slice(0, 16)}</span>
        {categories.map((name, i) => (
          <span key={`${id}cateogry${i}`}>
            <button className="btn-link">{name}</button>
            {i < categories.length - 1 ? " | " : ""}
          </span>
        ))}
      </div>
      {isViewingProject && (
        <div className="controls">
          {tab !== "library" && (
            <button
              className="btn btn-primary"
              onClick={() => changeArticleTab("library")}
            >
              Move to Library
            </button>
          )}
          {tab !== "feed" && (
            <button
              className="btn btn-primary"
              onClick={() => changeArticleTab("feed")}
            >
              Move to Feed
            </button>
          )}
          {tab !== "trash" && (
            <button className="btn" onClick={() => alert("To do")}>
              <i className="icon icon-delete"></i>
            </button>
          )}
        </div>
      )}
      <details className="accordion">
        <summary className="accordion-header">
          <i className="icon icon-arrow-right mr-1"></i>
          Summary
        </summary>
        <div className="accordion-body">{summary}</div>
      </details>
    </div>
  );
};

export default Article;
