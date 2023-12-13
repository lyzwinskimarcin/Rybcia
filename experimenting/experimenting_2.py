import numpy as np

babelki = sorted(root_node.children, key=lambda child: child.val, reverse=True)
        for _ in range(min(3, len(babelki))):
            print(_, ":")
            print(babelki[_].move)
            print(babelki[_].val)

        print(f"Feature been used: {self.feat_count} times.")