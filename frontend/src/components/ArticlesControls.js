import React from "react";
import { Link } from "react-router-dom";

const ArticlesControls = ({ activeTab, page, setPage, count }) => {
  const totalPages = count ? Math.ceil(count / 50) : "?";
  const hasPagesLeft = page > 0;
  const hasPagesRight = page + 1 < totalPages;
  return (
    <div className="space-between">
      <div className="tabs btn-group btn-group-block">
        <Link
          className={`btn ${activeTab === "articles" ? "active" : ""}`}
          to="/"
        >
          Articles
        </Link>
        <Link
          className={`btn ${activeTab === "library" ? "active" : ""}`}
          to="/library"
        >
          Libary
        </Link>
      </div>
      <div className="text-right page-controls">
        {count !== undefined && (
          <div className="text-center">{count} articles</div>
        )}
        <button disabled={!hasPagesLeft} onClick={() => setPage((p) => p - 1)}>
          <i className="icon icon-arrow-left" />
        </button>
        <span>
          Page {page + 1}/{totalPages}
        </span>
        <button disabled={!hasPagesRight} onClick={() => setPage((p) => p + 1)}>
          <i className="icon icon-arrow-right" />
        </button>
      </div>
    </div>
  );
};

export default ArticlesControls;
