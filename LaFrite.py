import io


class LaFrite():
    def __init__(self) -> None:
        super().__init__()
        self.im_lafrite = False
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'Libre Computer AML-S805X-AC'.lower() in m.read().lower():
                    self.im_lafrite = True
                    print("I`m La Frite")
        except Exception:
            pass
