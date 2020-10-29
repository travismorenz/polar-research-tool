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
      {isViewingProject && (
        <div className="form-group">
          <label
            className="form-radio form-inline"
            onClick={
              tab === "library" ? () => changeArticleTab("feed") : undefined
            }
          >
            <input
              type="radio"
              name={`${id}tab`}
              value="feed"
              checked={tab === "feed"}
              readOnly
            />
            <i className="form-icon"></i> Feed
          </label>
          <label
            className="form-radio form-inline"
            onClick={
              tab === "feed" ? () => changeArticleTab("library") : undefined
            }
          >
            <input
              type="radio"
              name={`${id}tab`}
              value="library"
              checked={tab === "library"}
              readOnly
            />
            <i className="form-icon"></i> Library
          </label>
        </div>
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
      <div className="metadata">
        <span className="publish_date">{publish_date.slice(0, 16)}</span>
        {categories.map((name, i) => (
          <span key={`${id}cateogry${i}`}>
            <button className="btn-link">{name}</button>
            {i < categories.length - 1 ? " | " : ""}
          </span>
        ))}
      </div>
      <details class="accordion">
        <summary class="accordion-header">
          <i class="icon icon-arrow-right mr-1"></i>
          Summary
        </summary>
        <div class="accordion-body">{summary}</div>
      </details>
    </div>
  );
};

export default Article;
