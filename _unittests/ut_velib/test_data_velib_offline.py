"""
@brief      test log(time=28s)
"""


import sys
import os
import unittest
import datetime
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from manydataapi.velib import DataCollectJCDecaux


class TestDataVelibOffline(ExtTestCase):

    def test_data_velib_contract(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")
        fold = os.path.abspath(os.path.split(__file__)[0])
        data = os.path.join(fold, "data")

        df = DataCollectJCDecaux.to_df(data)
        # fLOG(df.head())
        self.assertGreater(df.shape[0], 1)

        stations = df[["name", "lat", "lng"]]
        gr = stations.groupby(["name", "lat", "lng"], as_index=False).sum()
        # fLOG(gr.head())
        self.assertGreater(len(gr), 30)

        df.to_csv(os.path.join(fold, "out_data.txt"), sep="\t", index=False)
        dt = datetime.datetime(2014, 5, 22, 11, 49, 27, 523164)
        sub = df[df["collect_date"] == dt]
        _, __, plt = DataCollectJCDecaux.draw(sub)
        plt.close('all')

    def test_data_velib_animation_plt(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")
        fold = os.path.abspath(os.path.split(__file__)[0])
        data = os.path.join(fold, "data")

        if "travis" in sys.executable:
            return

        df = DataCollectJCDecaux.to_df(data)
        anim = DataCollectJCDecaux.animation(df)
        self.assertTrue(anim is not True)

    def test_data_velib_animation_moviepy(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")
        fold = os.path.abspath(os.path.split(__file__)[0])
        data = os.path.join(fold, "data")

        if "travis" in sys.executable:
            return

        df = DataCollectJCDecaux.to_df(data)
        anim = DataCollectJCDecaux.animation(df, module="moviepy")
        self.assertTrue(anim is not None)
        temp = get_temp_folder(__file__, "temp_moviepy")
        img = os.path.join(temp, "anim.gif")
        anim.write_gif(img, fps=20)
        self.assertTrue(os.path.exists(img))


if __name__ == "__main__":
    unittest.main()
