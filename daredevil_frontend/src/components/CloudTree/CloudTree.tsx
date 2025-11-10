import { TreeView, createTreeCollection } from "@chakra-ui/react"
import { LuFile, LuFolder } from "react-icons/lu"


export function CloudTree() {
  return (
    <TreeView.Root className="t-font" collection={collection} maxW="2xl">
      <TreeView.Label>Tree</TreeView.Label>
      <TreeView.Tree>
        <TreeView.Node
          indentGuide={<TreeView.BranchIndentGuide />}
          render={({ node, nodeState }) =>
            nodeState.isBranch ? (
              <TreeView.BranchControl>
                <LuFolder />
                <TreeView.BranchText>{node.name}</TreeView.BranchText>
              </TreeView.BranchControl>
            ) : (
              <TreeView.Item>
                <LuFile />
                <TreeView.ItemText>{node.name}</TreeView.ItemText>
              </TreeView.Item>
            )
          }
        />
      </TreeView.Tree>
    </TreeView.Root>
  )
}

interface Node {
  id: string
  name: string
  children?: Node[]
}

const collection = createTreeCollection<Node>({
  nodeToValue: (node) => node.id,
  nodeToString: (node) => node.name,
  rootNode: {
    id: "1",
    name: "application engineering",
    children: [
      {
        id: "2",
        name: "kanban board",
        children: [
          { id: "3", name: "backlog" },
          { id: "4", name: "discovery" },
          {
            id: "5", name: "current",
            children: [
              { id: "6", name: "backend development" },
              { id: "7", name: "database migration" },
            ],
          },
        ],
      },
      {
        id: "8",
        name: "CI/CD Docker Build",
        children: [
          { id: "9", name: "automated git actions" },
          { id: "10", name: "debugging & bug fixing" },
        ],
      },
      { id: "11", name: "code reviews" },
      { id: "12", name: "updating documentation" },
      { id: "13", name: "monitoring & logging" },
      { id: "14", name: "testing & deploying" },
    ],
  },
})
