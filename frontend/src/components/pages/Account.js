import { AppContext } from "components/pages/App";
import Project from "components/Project";
import ProjectControls from "components/ProjectControls";
import React, { useContext } from "react";
import { Redirect } from "react-router-dom";
import {
  addCategory as addCategoryService, addKeyphrase as addKeyphraseService,



  joinProject as joinProjectService,
  leaveProject as leaveProjectService, removeCategory as removeCategoryService, removeKeyphrase as removeKeyphraseService
} from "services/projects";


const AccountPage = () => {
  const {
    state: { isAdmin, projects, isLoggedIn },
    action,
  } = useContext(AppContext);

  // Must be logged in to view this page
  if (!isLoggedIn) return <Redirect to="/" />;

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

  const leaveProject = async ({ name, id }) => {
    await leaveProjectService(name);
    action("remove_project", id);
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
          leaveProject={leaveProject}
          key={project.id}
          {...project}
        />
      ))}
    </div>
  );
};

export default AccountPage;
