import React, { useEffect, useState, useRef } from "react";

const ArticlesControls = ({
  count,
  tab,
  setTab,
  page,
  setPage,
  showLibrary,
}) => {
  const [isSticky, setIsSticky] = useState(false);
  const ref = useRef(null);
  const handleScroll = () => {
    if (ref.current) {
      setIsSticky(ref.current.getBoundingClientRect().top <= 0);
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", () => handleScroll);
    };
  }, []);

  const totalPages = count ? Math.ceil(count / 50) : "?";
  const hasPagesLeft = page > 0;
  const hasPagesRight = page + 1 < totalPages;

  return (
    // All this sticky logic was stuck in haphazardly. I think the markup and styles can be cleaned up
    <div className={`sticky-wrapper ${isSticky ? "sticky" : ""}`} ref={ref}>
      <div className="sticky-inner">
        <div className="space-between container grid-lg">
          <div className="tabs btn-group btn-group-block">
            <button
              className={`btn ${tab === "feed" ? "active" : ""}`}
              onClick={() => {
                setPage(0);
                setTab("feed");
              }}
            >
              Feed
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
            <button
              disabled={!hasPagesLeft}
              onClick={() => setPage((p) => p - 1)}
            >
              <i className="icon icon-arrow-left" />
            </button>
            <span>
              Page {page + 1}/{totalPages}
            </span>
            <button
              disabled={!hasPagesRight}
              onClick={() => setPage((p) => p + 1)}
            >
              <i className="icon icon-arrow-right" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticlesControls;
