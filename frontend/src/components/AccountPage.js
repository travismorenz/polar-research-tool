import React, { useContext } from "react";

import Project from "./Project";
import {
  addKeyphrase as addKeyphraseService,
  removeKeyphrase as removeKeyphraseService,
  addCategory as addCategoryService,
  removeCategory as removeCategoryService,
  joinProject as joinProjectService,
} from "../services/projects";
import ProjectControls from "./ProjectControls";
import { AppContext } from "./App";

const AccountPage = () => {
  const {
    state: { isAdmin, projects },
    action,
  } = useContext(AppContext);

  const addKeyphrase = async (keyphrase, projectId) => {
    const project = projects[projectId];
    keyphrase = keyphrase.trim();
    if (!keyphrase || project.keyphrases.includes(keyphrase)) return;
    const { keyphrases } = await addKeyphraseService(keyphrase, projectId);
    action("set_keyphrases", { keyphrases, projectId });
  };

  const removeKeyphrase = async (keyphrase, projectId) => {
    keyphrase = keyphrase.trim();
    const { keyphrases } = await removeKeyphraseService(keyphrase, projectId);
    action("set_keyphrases", { keyphrases, projectId });
  };

  const addCategory = async (category, projectId) => {
    const project = projects[projectId];
    category = category.trim();
    if (!category || project.keyphrases.includes(category)) return;
    const { categories } = await addCategoryService(category, projectId);
    action("set_categories", { categories, projectId });
  };

  const removeCategory = async (category, projectId) => {
    category = category.trim();
    const { categories } = await removeCategoryService(category, projectId);
    action("set_categories", { categories, projectId });
  };

  const joinProject = async (projectName) => {
    const { newProject } = await joinProjectService(projectName);
    action("add_project", newProject);
  };

  return (
    <div className="container grid-lg">
      <h2>My Account</h2>
      <ProjectControls
        projects={projects}
        isAdmin={isAdmin}
        joinProject={joinProject}
      />
      <h4>Projects</h4>
      {Object.values(projects).map((project) => (
        <Project
          addKeyphrase={addKeyphrase}
          removeKeyphrase={removeKeyphrase}
          addCategory={addCategory}
          removeCategory={removeCategory}
          key={project.id}
          {...project}
        />
      ))}
    </div>
  );
};

export default AccountPage;
