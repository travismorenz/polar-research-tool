import React, { useState, useContext, useEffect } from "react";
import { usePaginatedQuery } from "react-query";

import Article from "components/Article";
import ArticleControls from "components/ArticleControls";
import { AppContext } from "components/pages/App";
import { getArticles } from "services/getArticles";
import toggleArticleInLibrary from "services/toggleArticleInLibrary";

const ArticlesPage = () => {
  const {
    state: { selectedProjectId, projects },
    action,
  } = useContext(AppContext);
  const [tab, setTab] = useState("articles");
  const [page, setPage] = useState(0);

  const { latestData, isLoading, error, isFetching } = usePaginatedQuery(
    ["articles", selectedProjectId, page],
    getArticles
  );

  // Set the page to 0 when changing projects
  useEffect(() => {
    setPage(0);
    setTab("articles");
  }, [selectedProjectId, tab]);

  // Set the page to 0 when changing tabs
  useEffect(() => {
    if (tab === "library") {
      setPage(0);
    }
  }, [tab]);

  if (!latestData || isLoading) {
    return <div className="loading loading-lg"></div>;
  }

  if (error) {
    console.log(error);
    return <div>There was an error retrieving the data. Check console.</div>;
  }

  // const toggleInLibrary = async (article_id) => {
  //   await toggleArticleInLibrary(selectedProjectId, article_id);
  //   action("toggle_in_library", {
  //     projectId: selectedProjectId,
  //     articleId: article_id,
  //   });
  // };

  return (
    <div className="container grid-lg">
      <ArticleControls
        tab={tab}
        setTab={setTab}
        page={page}
        setPage={setPage}
        totalCount={latestData.count}
        // libraryCount={libraryIds.length}
      />
      {Object.values(latestData.articles).map((article) => (
        <Article
          key={article.id}
          // inLibrary={libraryIds.includes(article.id)}
          // toggleInLibrary={toggleInLibrary}
          onProjectPage={selectedProjectId !== "_default"}
          {...article}
        />
      ))}
    </div>
  );
};

export default ArticlesPage;
