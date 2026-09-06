# tests/core/docker/test_service.py

"""
Tests for DockerService.

This module tests Docker business logic.
"""

from unittest.mock import Mock

import pytest

from app.core.docker.service import DockerService
from app.core.shared import DockerOperationError


class TestDockerService:
    """
    Tests for DockerService.
    """

    @pytest.fixture
    def executor(self):
        """
        Create a mock Docker executor.
        """
        return Mock()

    @pytest.fixture
    def service(
        self,
        executor,
    ):
        """
        Create DockerService instance.
        """
        return DockerService(
            executor=executor,
        )

    # =====================================================
    # Build Image
    # =====================================================

    def test_build_image_success(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should build image successfully.
        """
        executor.build_image.return_value = success_result

        service.build_image(
            "example",
            "latest",
        )

        executor.build_image.assert_called_once()

    def test_build_image_raises_docker_operation_error(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should raise DockerOperationError when build fails.
        """
        executor.build_image.return_value = failed_result

        with pytest.raises(
            DockerOperationError,
        ):
            service.build_image(
                "example",
                "latest",
            )

    # =====================================================
    # Tag Image
    # =====================================================

    def test_tag_image_success(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should tag image successfully.
        """
        executor.tag_image.return_value = success_result

        service.tag_image(
            "example",
            "latest",
            "v1.0.0",
        )

        executor.tag_image.assert_called_once()

    def test_tag_image_raises_docker_operation_error(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should raise DockerOperationError when tagging fails.
        """
        executor.tag_image.return_value = failed_result

        with pytest.raises(
            DockerOperationError,
        ):
            service.tag_image(
                "example",
                "latest",
                "v1.0.0",
            )

    # =====================================================
    # Push Image
    # =====================================================

    def test_push_image_success(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should push image successfully.
        """
        executor.push_image.return_value = success_result

        service.push_image(
            "example",
            "latest",
        )

        executor.push_image.assert_called_once()

    def test_push_image_raises_docker_operation_error(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should raise DockerOperationError when push fails.
        """
        executor.push_image.return_value = failed_result

        with pytest.raises(
            DockerOperationError,
        ):
            service.push_image(
                "example",
                "latest",
            )

    # =====================================================
    # Remove Local Image
    # =====================================================

    def test_remove_local_image(
        self,
        service,
        executor,
    ):
        """
        Should delegate image removal.
        """
        service.remove_local_image(
            "example",
            "latest",
        )

        executor.remove_local_image.assert_called_once_with(
            image="example",
            tag="latest",
        )

    # =====================================================
    # Dry Run
    # =====================================================

    def test_get_is_dry_run(
        self,
        service,
        executor,
    ):
        """
        Should return executor dry-run state.
        """
        executor.get_is_dry_run.return_value = True

        assert service.get_is_dry_run() is True

    def test_set_is_dry_run(
        self,
        service,
        executor,
    ):
        """
        Should delegate dry-run state.
        """
        service.set_is_dry_run(True)

        executor.set_is_dry_run.assert_called_once_with(True)

    # =====================================================
    # Silent
    # =====================================================

    def test_get_silent(
        self,
        service,
        executor,
    ):
        """
        Should return executor silent state.
        """
        executor.get_silent.return_value = True

        assert service.get_silent() is True

    def test_set_silent(
        self,
        service,
        executor,
    ):
        """
        Should delegate silent state.
        """
        service.set_silent(True)

        executor.set_silent.assert_called_once_with(True)
