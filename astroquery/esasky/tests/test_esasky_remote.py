# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os
import shutil
import pytest

from astroquery.utils.commons import TableList

from ... import esasky

ESASkyClass = esasky.core.ESASkyClass()


@pytest.mark.remote_data
class TestESASky:
    ESASkyClass._isTest = "Remote Test"

    def test_esasky_query_region_maps(self):
        result = ESASkyClass.query_region_maps("M51", "5 arcmin")
        assert isinstance(result, TableList)

    def test_esasky_query_object_maps(self):
        result = ESASkyClass.query_object_maps("M51")
        assert isinstance(result, TableList)

    @pytest.mark.bigdata
    def test_esasky_get_images(self):
        download_directory = "ESASkyRemoteTest"
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        missions = ESASkyClass.list_maps()
        # Remove very large map missions & missions with many results
        # & missions without proper download url (INTEGRAL, SUZAKU, ALMA, AKARI)
        missions = [mission for mission in missions if mission not in
                    ("HST-OPTICAL", "HST-IR", "HST-UV", "XMM-OM-UV", "INTEGRAL", "SUZAKU", "ALMA", "AKARI")]

        ESASkyClass.get_images("M51", missions=missions, download_dir=download_directory)

        for mission in missions:
            file_path = os.path.join(download_directory, mission)
            assert os.path.exists(file_path)

        shutil.rmtree(download_directory)

    def test_esasky_get_images_small(self):
        download_directory = "ESASkyRemoteTest"
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        # ISO is only ~ 163 kB
        missions = ['ISO-IR']

        ESASkyClass.get_images("M6", radius="12arcmin", missions=missions, download_dir=download_directory)

        for mission in missions:
            file_path = os.path.join(download_directory, mission)
            assert os.path.exists(file_path)

        shutil.rmtree(download_directory)

    @pytest.mark.bigdata
    def test_esasky_get_images_hst(self):
        download_directory = "ESASkyRemoteTest"
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        ESASkyClass.get_images("M11", radius="2.1 deg", missions="HST-UV", download_dir=download_directory)

        file_path = os.path.join(download_directory, "HST-UV")
        assert os.path.exists(file_path)

        shutil.rmtree(download_directory)

    def test_esasky_query_region_catalogs(self):
        result = ESASkyClass.query_region_catalogs("M51", "5 arcmin")
        assert isinstance(result, TableList)

    def test_esasky_query_object_catalogs(self):
        result = ESASkyClass.query_object_catalogs("M51")
        assert isinstance(result, TableList)

    def test_esasky_get_maps(self):
        download_directory = "ESASkyRemoteTest"
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        file_path = os.path.join(download_directory, 'ISO-IR')

        all_maps = ESASkyClass.query_object_maps("M51")
        isomaps = ESASkyClass.query_object_maps("M51", missions='ISO-IR')
        # Remove a few maps, so the other list will have downloadable ones, too
        isomaps['ISO-IR'].remove_rows([0, 1])
        ESASkyClass.get_maps(isomaps, download_dir=download_directory)
        assert len(os.listdir(file_path)) == len(all_maps['ISO-IR']) - 2

        isomaps2 = dict({'ISO-IR': all_maps['ISO-IR'][:2]})
        ESASkyClass.get_maps(isomaps2, download_dir=download_directory)
        assert len(os.listdir(file_path)) == len(all_maps['ISO-IR'])

        shutil.rmtree(download_directory)
