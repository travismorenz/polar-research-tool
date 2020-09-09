import React, { useEffect, useState } from "react";

import { getAllProjectNames } from "services/projects";

const ProjectControls = ({ projects, isAdmin, joinProject }) => {
  const [allProjects, setAllProjects] = useState([]);
  const [selection, setSelection] = useState(0);
  useEffect(() => {
    const init = async () => {
      const res = await getAllProjectNames();
      setAllProjects(res.projectNames);
    };
    init();
  }, []);

  const options = allProjects.filter((name) =>
    Object.values(projects).every((p) => p.name !== name)
  );

  return (
    <div className="form-group project-controls">
      {isAdmin && "Admin controls will go here"}
      <h5>Join Project</h5>
      <label className="form-inline">
        {options.length ? (
          <>
            <select
              className="form-select"
              id="project-select"
              value={selection}
              onChange={(e) => setSelection(e.target.value)}
            >
              {options.map((name, i) => (
                <option value={i} key={i}>
                  {name}
                </option>
              ))}
            </select>
            <button
              className="btn btn-primary"
              onClick={() => joinProject(options[selection])}
            >
              Join Project
            </button>
          </>
        ) : (
          "You have joined all available proejcts"
        )}
      </label>
    </div>
  );
};

export default ProjectControls;
