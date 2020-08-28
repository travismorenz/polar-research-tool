import React, { useContext } from "react";

import Project from "./Project";
import { AppContext } from "./App";

const AccountPage = () => {
  const {
    state: { isAdmin, projects },
    action,
  } = useContext(AppContext);

  const addKeyphrase = (keyphrase, projectId) => {
    const project = projects[projectId];
    keyphrase = keyphrase.trim();
    if (project.keyphrases.includes(keyphrase)) return;
  };

  return (
    <div className="container grid-lg">
      <h2>My Account</h2>
      <h4>Projects</h4>
      {Object.values(projects).map((project) => (
        <Project addKeyphrase={addKeyphrase} key={project.id} {...project} />
      ))}
    </div>
  );
};

export default AccountPage;
