import './Home.scss';
import reactUrl from "./assets/react.svg"
import rubyUrl from "./assets/ruby.svg"
import docsUrl from "./assets/documentation.svg";
import designUrl from "./assets/design.svg";

import { Link } from "react-router-dom";
import { Button } from "@progress/kendo-react-buttons";
import {
  AppBar,
  AppBarSection,
  AppBarSpacer,
  Card,
  CardActions,
  CardBody,
  CardHeader,
  CardTitle
} from "@progress/kendo-react-layout";

export default function Home() {
  return (
    <>
      <AppBar position="top">
        <AppBarSection>Daredevil 🩸 Deployer</AppBarSection>
        <AppBarSpacer />
        <AppBarSection>
          <Link to="/">
            <Button themeColor="primary" fillMode="flat" className="k-mr-1">Home</Button>
          </Link>
          <Link to="/dashboard/">
            <Button themeColor="primary" fillMode="flat">Dashboard</Button>
          </Link>
        </AppBarSection>
      </AppBar>

      <section className="section-container">
        <img src={rubyUrl} alt="React Logo" className="ruby-logo" />
        <div className="k-d-flex k-flex-col k-my-12">
          <h1 className="welcome-title">Welcome to Daredevil Deployer</h1>
          <h3 className="welcome-subtitle">Deploying Apps</h3>

          <div className="k-mt-3">
            <Button themeColor="primary" className="k-mr-2">
              <a href="https://www.notion.com/" target="_blank">Notion Docs</a>
            </Button>
            <Button themeColor="secondary" fillMode="solid">
              <a href="https://firecracker-microvm.github.io/" target="_blank">Firecracker</a>
            </Button>
          </div>
        </div>
      </section>
      <section className="section-container get-started">
        <div className="center-section">
          <h5 className="section-title">Welcome Welcome Welcome</h5>
          <div className="k-ml-2"><code>using the github api</code></div>
        </div>
      </section>
      <section className="section-container">
        <div className="cards">
          <h5 className="section-title">Highlights</h5>
          <div className="cards-container">
            <Card>
              <CardHeader>
                <img src={docsUrl} alt="Documentation Logo" width={64} height={64} />
                <CardTitle>Documentation</CardTitle>
              </CardHeader>
              <CardBody>
                <p>
                  In development ...
                </p>
              </CardBody>
              <CardActions>
                <Button themeColor="primary" fillMode="flat">
                  <a href="https://textual.textualize.io/" target="_blank">Textual</a>
                </Button>
              </CardActions>
            </Card>

            <Card>
              <CardHeader>
                <img src={reactUrl} alt="Virtual Classroom Logo" width={64} height={64} />
                <CardTitle>Using React.js</CardTitle>
              </CardHeader>
              <CardBody>
                <p>
                  Using nvim editor ...
                </p>
              </CardBody>
              <CardActions>
                <Button themeColor="primary" fillMode="flat">
                  <a href="https://docs.anthropic.com/en/home" target="_blank">Claude Code</a>
                </Button>
              </CardActions>
            </Card>

            <Card>
              <CardHeader>
                <img src={designUrl} alt="Design System Logo" width={64} height={64} />
                <CardTitle>Design System</CardTitle>
              </CardHeader>
              <CardBody>
                <p>
                  Quickly apply harmonious and consistent styles to the components in your app with the Progress Design System.
                </p>
              </CardBody>
              <CardActions>
                <Button themeColor="primary" fillMode="flat">
                  <a href="https://www.telerik.com/design-system/docs/" target="_blank">Design Style</a>
                </Button>
              </CardActions>
            </Card>

            <Card>
              <CardHeader>
                <img src={rubyUrl} alt="License Logo" width={64} height={64} />

                <CardTitle>Ruby on Rails</CardTitle>
              </CardHeader>
              <CardBody>
                <ul className="card-list">
                  <li>Ruby</li>
                  <li>Python</li>
                  <li>Javascript</li>
                  <li>Bash</li>
                </ul>
              </CardBody>
              <CardActions>
                <Button themeColor="primary" fillMode="flat">
                  <a href="https://podman.io/" target="_blank">Podman Container Tools</a>
                </Button>
              </CardActions>
            </Card>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div>Operational ⊛ 2025 Woodford's Den Software. All rights reserved.</div>
      </footer>
    </>
  )
}
