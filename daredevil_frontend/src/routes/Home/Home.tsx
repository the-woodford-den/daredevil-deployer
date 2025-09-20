import './Home.scss';
import reactUrl from "../../assets/react.svg"
import rubyUrl from "../../assets/ruby.svg"
import docsUrl from "../../assets/documentation.svg";
import designUrl from "../../assets/design.svg";

import { Button } from "@progress/kendo-react-buttons";
import {
  Card,
  CardActions,
  CardBody,
  CardHeader,
  CardTitle,
  GridLayout,
  GridLayoutItem
} from "@progress/kendo-react-layout";

export default function Home() {
  return (
    <>
      <GridLayout
        align={{ horizontal: 'center', vertical: 'middle' }}
        cols={[{ width: '33.33%' }, { width: '33.34%' }, { width: '33.33%' }]}
      >
        <GridLayoutItem colSpan={2}>
          <section className="section-container">
            <img src={rubyUrl} alt="React Logo" className="ruby-logo" />
            <div className="k-d-flex k-flex-col k-my-12">
              <h1 className="welcome-title">Welcome to Daredevil Deployer</h1>
              <h3 className="welcome-subtitle">Deploying Apps</h3>
            </div>
          </section>
        </GridLayoutItem>
        <GridLayoutItem>
          <div className="k-mt-3">
            <Button themeColor="secondary" fillMode="solid">
              <a href="https://www.notion.com/" target="_blank">Notion Docs</a>
            </Button>
            <Button themeColor="secondary" fillMode="solid">
              <a href="https://firecracker-microvm.github.io/" target="_blank">Firecracker</a>
            </Button>
          </div>
        </GridLayoutItem>
        <GridLayoutItem colSpan={3}>
          <section className="section-container get-started">
            <div className="center-section">
              <h5 className="section-title">Welcome Welcome Welcome</h5>
              <div className="k-ml-2"><code>using the github api</code></div>
            </div>
          </section>
        </GridLayoutItem>
      </GridLayout>
      <GridLayout
        align={{ horizontal: 'center', vertical: 'middle' }}
        cols={[{ width: '16.67%' }, { width: '16.67%' }, { width: '16.66%' }, { width: '16.66%' }, { width: '16.67%' }, { width: '16.67%' }]}
      >
        <GridLayoutItem colSpan={6}>
          <h5 className="section-title">Highlights</h5>
        </GridLayoutItem>
        <GridLayoutItem></GridLayoutItem>
        <GridLayoutItem>
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
        </GridLayoutItem>
        <GridLayoutItem>
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
        </GridLayoutItem>
        <GridLayoutItem>
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
        </GridLayoutItem>
        <GridLayoutItem>
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
        </GridLayoutItem>
      </GridLayout>
    </>
  )
}
