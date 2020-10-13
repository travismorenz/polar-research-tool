import React from "react";

const ArticlesControls = ({
  count,
  tab,
  setTab,
  page,
  setPage,
  showLibrary,
}) => {
  const totalPages = count ? Math.ceil(count / 50) : "?";
  const hasPagesLeft = page > 0;
  const hasPagesRight = page + 1 < totalPages;
  return (
    <div className="space-between">
      <div className="tabs btn-group btn-group-block">
        <button
          className={`btn ${tab === "articles" ? "active" : ""}`}
          onClick={() => {
            setPage(0);
            setTab("articles");
          }}
        >
          Articles
        </button>
        {showLibrary && (
          <button
            className={`btn ${tab === "library" ? "active" : ""}`}
            onClick={() => {
              setPage(0);
              setTab("library");
            }}
          >
            Libary
          </button>
        )}
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
