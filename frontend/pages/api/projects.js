const sampleProjects = [
  { projectId: 'foo', name: 'Foo' },
  { projectId: 'bar', name: 'Bar' },
]

export default function(req, res) {
  res.status(200).json({ projects: sampleProjects })
}
