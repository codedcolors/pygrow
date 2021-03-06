from grow.pods import pods
from grow.pods import storage
from grow.pods.controllers import static
from grow.testing import testing
import os
import unittest


class PodTest(unittest.TestCase):

  def setUp(self):
    self.dir_path = testing.create_test_pod_dir()
    self.pod = pods.Pod(self.dir_path, storage=storage.FileStorage)

  def test_eq(self):
    pod = pods.Pod(self.dir_path, storage=storage.FileStorage)
    self.assertEqual(self.pod, pod)

  def test_list_dir(self):
    dirpath = os.path.join(self.dir_path, 'content')
    num_files = 0
    for root, dirs, files in os.walk(dirpath):
      for filename in files:
        num_files += 1
    actual = self.pod.list_dir('/content')
    self.assertEqual(len(actual), num_files)

  def test_read_file(self):
    content = self.pod.read_file('/README.md')
    path = os.path.join(self.dir_path, 'README.md')
    expected_content = open(path).read()
    self.assertEqual(expected_content, content)

  def test_write_file(self):
    path = '/dummy.yaml'
    self.pod.write_file(path, 'foo')
    content = self.pod.read_file(path)
    self.assertEqual('foo', content)

    self.pod.write_file(path, 'bar')
    content = self.pod.read_file(path)
    self.assertEqual('bar', content)

  def test_list_collections(self):
    self.pod.list_collections()

  def test_export(self):
    self.pod.export()

  def test_dump(self):
    paths = [
        '/about/index.html',
        '/app/static/somepath/de_alias/test.txt',
        '/app/static/test.txt',
        '/de_alias/about/index.html',
        '/de_alias/contact-us/index.html',
        '/de_alias/home/index.html',
        '/de_alias/html/index.html',
        '/de_alias/intro/index.html',
        '/de_alias/yaml_test/index.html',
        '/fr/about/index.html',
        '/fr/contact-us/index.html',
        '/fr/home/index.html',
        '/fr/html/index.html',
        '/fr/intro/index.html',
        '/fr/yaml_test/index.html',
        '/html/index.html',
        '/index.html',
        '/intl/de_alias/localized/index.html',
        '/intl/de_alias/multiple-locales/index.html',
        '/intl/en_gb/localized/index.html',
        '/intl/fr/multiple-locales/index.html',
        '/intl/hi_in/localized/index.html',
        '/intl/it/multiple-locales/index.html',
        '/intro/index.html',
        '/it/about/index.html',
        '/it/contact-us/index.html',
        '/it/home/index.html',
        '/it/html/index.html',
        '/it/intro/index.html',
        '/it/yaml_test/index.html',
        '/post/newer/index.html',
        '/post/newest/index.html',
        '/post/older/index.html',
        '/post/oldest/index.html',
        '/public/file.txt',
        '/public/main.css',
        '/public/main.min.js',
        '/root/base/index.html',
        '/root/static/file.txt',
        '/yaml_test/index.html',
    ]
    result = self.pod.dump()
    self.assertItemsEqual(paths, result)

  def test_to_message(self):
    self.pod.to_message()

  def test_list_deployments(self):
    self.pod.list_deployments()

  def test_get_home_doc(self):
    home_doc = self.pod.get_home_doc()
    doc = self.pod.get_doc('/content/pages/home.yaml')
    self.assertEqual(home_doc, doc)

  def test_get_static(self):
    static_file = self.pod.get_static('/public/file.txt')
    self.assertEqual('file', static_file.base)
    self.assertTrue(static_file.exists)
    self.assertRaises(
        static.BadStaticFileError, self.pod.get_static,
        '/bad-path/bad-file.txt')

  def test_list_statics(self):
    items = self.pod.list_statics('/public/')
    expected = [
        self.pod.get_static('/public/.dummy_dot_file'),
        self.pod.get_static('/public/file.txt'),
        self.pod.get_static('/public/main.css'),
        self.pod.get_static('/public/main.min.js'),
    ]
    for item in items:
      self.assertIn(item, expected)


if __name__ == '__main__':
  unittest.main()
