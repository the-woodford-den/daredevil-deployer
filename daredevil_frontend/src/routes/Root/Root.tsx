import { Link, Outlet } from 'react-router-dom';
import { Button } from "@progress/kendo-react-buttons";
import {
  AppBar,
  AppBarSection,
  AppBarSpacer
} from '@progress/kendo-react-layout';
import { Typography } from '@progress/kendo-react-common';
import bricolageLicense from "../../assets/Bricolage/Grotesque/2025-9-15/license.md?url";
import texturinaLicense from "../../assets/Texturina/2025-9-15/license.md?url";

function Root() {
  return (
    <>
      <AppBar themeColor="primary" position="top">
        <AppBarSection>Daredevil 🩸 Deployer</AppBarSection>
        <AppBarSpacer />
        <AppBarSection>
          <Link to="/">
            <Button themeColor="primary" fillMode="flat" className="k-mr-1">Home</Button>
          </Link>
          <Link to="/repositories">
            <Button themeColor="primary" fillMode="flat" className="k-mr-1">My Repos</Button>
          </Link>
        </AppBarSection>
      </AppBar>
      <Outlet />
      <footer>
        <div>
          <Typography.p textAlign={'center'}>
            Operational ~ 2025 Woodford's Den ~ <span>
              Licenses: </span>
            <a href={bricolageLicense} target="_blank" rel="noopener noreferrer">Bricolage Grotesque</a>
            <span> & </span>
            <a href={texturinaLicense} target="_blank" rel="noopener noreferrer">Texturina</a>
          </Typography.p>
        </div>
      </footer>
    </>
  );
}

export default Root;

