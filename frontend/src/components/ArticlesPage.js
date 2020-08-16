import React, { useState, useContext, useEffect } from "react";

import Article from "./Article";
import ArticlesControls from "./ArticlesControls";
import { AppContext } from "./App";
import { getArticleIds, getArticlesById } from "../services/getArticles";

// TODO: library/register/account

const PAGE_SIZE = 50;

const ArticlesPage = () => {
  const [page, setPage] = useState(0);
  const {
    state: { selectedProjectId, projects, articles },
    action,
  } = useContext(AppContext);
  const projectPage = projects[selectedProjectId].pages[page];
  const hasAllArticles = projectPage && projectPage.every((id) => articles[id]);

  // Load the article ids for each project and separate them into pages
  useEffect(() => {
    const loadArticleIds = async (projectId) => {
      action("set_project_loading", { projectId, bool: true });
      const { ids } = await getArticleIds(projectId);
      const count = ids.length;
      const pages = [];
      for (let i = 0; i < Math.ceil(count / PAGE_SIZE); i++) {
        pages.push(ids.slice(i * PAGE_SIZE, i * PAGE_SIZE + PAGE_SIZE));
      }
      action("set_pages_loaded", { projectId, pages, count });
      action("set_project_loading", { projectId, bool: false });
    };
    for (let project of Object.values(projects)) {
      if (!project.isLoading && !project.pages.length)
        loadArticleIds(project.id);
    }
  }, [projects, action]);

  // Load articles that are needed for each page
  useEffect(() => {
    const loadArticles = async () => {
      const neededIds = projects[selectedProjectId].pages[page].filter(
        (id) => !articles[id]
      );
      if (neededIds.length) {
        action("set_project_loading", {
          projectId: selectedProjectId,
          bool: true,
        });
        const newArticles = await getArticlesById(neededIds);
        action("add_articles", newArticles);
        action("set_project_loading", {
          projectId: selectedProjectId,
          bool: false,
        });
      }
    };
    // Only load articles if the page exists (i.e the ids have been loaded)
    // and if the articles/ids for that page are not currently being loaded
    if (
      projects[selectedProjectId].pages[page] &&
      !projects[selectedProjectId].isLoading
    )
      loadArticles();
  }, [articles, action, projects, page, selectedProjectId]);

  // Set the page to 0 when changing projects
  useEffect(() => setPage(0), [selectedProjectId]);

  return (
    <div className="container grid-lg">
      <ArticlesControls
        activeTab="articles"
        page={page}
        setPage={setPage}
        count={projects[selectedProjectId].count}
      />
      {hasAllArticles ? (
        projectPage.map((id) => <Article key={id} {...articles[id]} />)
      ) : (
        <div className="loading loading-lg"></div>
      )}
    </div>
  );
};

export default ArticlesPage;
