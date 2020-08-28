import React, { useContext } from "react";

import Project from "./Project";
import {
  addKeyphrase as addKeyphraseService,
  removeKeyphrase as removeKeyphraseService,
} from "../services/projects";
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
    const project = projects[projectId];
    keyphrase = keyphrase.trim();
    const { keyphrases } = await removeKeyphraseService(keyphrase, projectId);
    action("set_keyphrases", { keyphrases, projectId });
  };

  return (
    <div className="container grid-lg">
      <h2>My Account</h2>
      <h4>Projects</h4>
      {Object.values(projects).map((project) => (
        <Project
          addKeyphrase={addKeyphrase}
          removeKeyphrase={removeKeyphrase}
          key={project.id}
          {...project}
        />
      ))}
    </div>
  );
};

export default AccountPage;
