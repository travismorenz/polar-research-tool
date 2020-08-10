import React, { useState, useContext, useEffect } from "react";

import Article from "./Article";
import ArticlesControls from "./ArticlesControls";
import { AppContext } from "./App";
import { getArticleIds, getArticlesById } from "../services/getArticles";

// TODO: Preload all ids initially, load project ids in the background. Prevent changing to project until loaded.
// TODO: library/register/account
// TODO: as a part of register, remove unnecessary server side validation. Let frontend deal with all that

const ArticlesPage = () => {
  const [page, setPage] = useState(0);
  const {
    state: { selectedProjectId, projects, articles },
    action,
  } = useContext(AppContext);
  // const selectedProject = projects[selectedProjectId];
  const projectPage = false;

  // useEffect(() => {
  //   const loadArticles = async () => {
  //     setIsLoading(true);
  //     const { ids, count } = await getArticlesByProject(
  //       selectedProjectId,
  //       page
  //     );
  //     const neededArticles = ids.filter((id) => !articles[id]);
  //     if (neededArticles.length) {
  //       const newArticles = await getArticlesById(neededArticles);
  //       action("add_articles", { page, articles: newArticles });
  //     }
  //     action("set_count", count);
  //     setIsLoading(false);
  //   };
  //   // Load articles if current page hasn't been loaded and isn't being loaded
  //   if (!projects[selectedProjectId].pages[page] && !isLoading) loadArticles();
  // }, [action, articles, isLoading, page, projects, selectedProjectId]);

  // Load the article ids for each project and separate them into pages
  useEffect(() => {
    const loadArticleIds = async (projectId) => {
      action("set_pages_loading", projectId);
      const { ids } = await getArticleIds(projectId);
      const count = ids.length;
      const pages = [];
      for (let i = 0; i < Math.ceil(count / 50); i++) {
        pages.push(ids.slice(i * 50, i * 50 + 50));
      }
      action("set_pages_loaded", { projectId, pages, count });
    };
    for (let project of Object.values(projects)) {
      if (project.isLoading || project.pages.length) continue;
      loadArticleIds(project.id);
    }
  }, [projects, action]);

  useEffect(() => setPage(0), [selectedProjectId]);

  return (
    <div className="container grid-lg">
      <ArticlesControls
        activeTab="articles"
        page={page}
        setPage={setPage}
        count={false}
      />
      {projectPage ? (
        projectPage.map((id) => <Article key={id} {...articles[id]} />)
      ) : (
        <div className="loading loading-lg"></div>
      )}
    </div>
  );
};

export default ArticlesPage;
