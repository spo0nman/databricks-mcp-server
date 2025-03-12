"""
Router for cluster management endpoints.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

from src.api import clusters
from src.core.auth import validate_api_key
from src.core.utils import DatabricksAPIError, format_response

# Create router
router = APIRouter()


# Models
class ClusterConfig(BaseModel):
    """Cluster configuration model."""
    
    cluster_name: str = Field(..., description="Cluster name")
    spark_version: str = Field(..., description="Spark version")
    node_type_id: str = Field(..., description="Node type ID")
    num_workers: Optional[int] = Field(None, description="Number of workers")
    autotermination_minutes: Optional[int] = Field(
        60, description="Auto-termination minutes"
    )
    spark_conf: Optional[Dict[str, str]] = Field(
        None, description="Spark configuration"
    )
    aws_attributes: Optional[Dict[str, Any]] = Field(
        None, description="AWS attributes"
    )
    azure_attributes: Optional[Dict[str, Any]] = Field(
        None, description="Azure attributes"
    )
    driver_node_type_id: Optional[str] = Field(
        None, description="Driver node type ID"
    )
    ssh_public_keys: Optional[List[str]] = Field(
        None, description="SSH public keys"
    )
    custom_tags: Optional[Dict[str, str]] = Field(
        None, description="Custom tags"
    )
    cluster_log_conf: Optional[Dict[str, Any]] = Field(
        None, description="Cluster log configuration"
    )
    init_scripts: Optional[List[Dict[str, Any]]] = Field(
        None, description="Init scripts"
    )
    spark_env_vars: Optional[Dict[str, str]] = Field(
        None, description="Spark environment variables"
    )
    autoscale: Optional[Dict[str, int]] = Field(
        None, description="Autoscale configuration"
    )
    enable_elastic_disk: Optional[bool] = Field(
        None, description="Enable elastic disk"
    )
    instance_pool_id: Optional[str] = Field(
        None, description="Instance pool ID"
    )
    policy_id: Optional[str] = Field(
        None, description="Policy ID"
    )
    
    class Config:
        """Pydantic configuration."""
        
        schema_extra = {
            "example": {
                "cluster_name": "my-cluster",
                "spark_version": "10.4.x-scala2.12",
                "node_type_id": "Standard_D3_v2",
                "num_workers": 2,
                "autotermination_minutes": 60,
                "spark_conf": {
                    "spark.speculation": "true"
                },
                "azure_attributes": {
                    "availability": "ON_DEMAND_AZURE"
                }
            }
        }


class ClusterResponse(BaseModel):
    """Cluster response model."""
    
    cluster_id: str = Field(..., description="Cluster ID")


class ClusterInfo(BaseModel):
    """Cluster information model."""
    
    cluster_id: str = Field(..., description="Cluster ID")
    cluster_name: str = Field(..., description="Cluster name")
    state: str = Field(..., description="Cluster state")
    creator_user_name: str = Field(..., description="Creator username")
    spark_version: str = Field(..., description="Spark version")
    node_type_id: str = Field(..., description="Node type ID")
    driver_node_type_id: Optional[str] = Field(
        None, description="Driver node type ID"
    )
    autotermination_minutes: Optional[int] = Field(
        None, description="Auto-termination minutes"
    )
    num_workers: Optional[int] = Field(None, description="Number of workers")
    autoscale: Optional[Dict[str, int]] = Field(
        None, description="Autoscale configuration"
    )
    state_message: Optional[str] = Field(None, description="State message")
    spark_context_id: Optional[str] = Field(
        None, description="Spark context ID"
    )
    jdbc_port: Optional[int] = Field(None, description="JDBC port")
    cluster_memory_mb: Optional[int] = Field(
        None, description="Cluster memory in MB"
    )
    cluster_cores: Optional[float] = Field(
        None, description="Cluster cores"
    )
    default_tags: Optional[Dict[str, str]] = Field(
        None, description="Default tags"
    )
    custom_tags: Optional[Dict[str, str]] = Field(
        None, description="Custom tags"
    )
    cluster_log_conf: Optional[Dict[str, Any]] = Field(
        None, description="Cluster log configuration"
    )
    init_scripts: Optional[List[Dict[str, Any]]] = Field(
        None, description="Init scripts"
    )
    spark_env_vars: Optional[Dict[str, str]] = Field(
        None, description="Spark environment variables"
    )
    spark_conf: Optional[Dict[str, str]] = Field(
        None, description="Spark configuration"
    )
    azure_attributes: Optional[Dict[str, Any]] = Field(
        None, description="Azure attributes"
    )
    driver: Optional[Dict[str, Any]] = Field(
        None, description="Driver information"
    )
    executors: Optional[List[Dict[str, Any]]] = Field(
        None, description="Executors information"
    )
    start_time: Optional[int] = Field(None, description="Start time")
    terminated_time: Optional[int] = Field(None, description="Terminated time")
    last_state_loss_time: Optional[int] = Field(
        None, description="Last state loss time"
    )
    last_activity_time: Optional[int] = Field(
        None, description="Last activity time"
    )
    cluster_source: Optional[str] = Field(None, description="Cluster source")
    instance_pool_id: Optional[str] = Field(
        None, description="Instance pool ID"
    )
    policy_id: Optional[str] = Field(None, description="Policy ID")
    single_user_name: Optional[str] = Field(
        None, description="Single user name"
    )
    enable_elastic_disk: Optional[bool] = Field(
        None, description="Enable elastic disk"
    )
    disk_spec: Optional[Dict[str, Any]] = Field(
        None, description="Disk specification"
    )
    data_security_mode: Optional[str] = Field(
        None, description="Data security mode"
    )
    runtime_engine: Optional[str] = Field(None, description="Runtime engine")
    effective_spark_version: Optional[str] = Field(
        None, description="Effective Spark version"
    )


class ClustersList(BaseModel):
    """Clusters list model."""
    
    clusters: List[ClusterInfo] = Field(..., description="List of clusters")


# Endpoints
@router.post(
    "/create",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new cluster",
    description="Create a new Databricks cluster with the specified configuration.",
)
async def create_cluster(
    config: ClusterConfig,
    api_key: Dict[str, Any] = Depends(validate_api_key),
) -> Dict[str, Any]:
    """
    Create a new Databricks cluster.
    
    Args:
        config: Cluster configuration
        api_key: API key for authentication
        
    Returns:
        Response containing the cluster ID
        
    Raises:
        HTTPException: If the API request fails
    """
    try:
        response = await clusters.create_cluster(config.dict(exclude_none=True))
        return format_response(success=True, data=response, status_code=201)
    except DatabricksAPIError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/terminate",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Terminate a cluster",
    description="Terminate a running Databricks cluster.",
)
async def terminate_cluster(
    cluster_id: str,
    api_key: Dict[str, Any] = Depends(validate_api_key),
) -> Dict[str, Any]:
    """
    Terminate a Databricks cluster.
    
    Args:
        cluster_id: ID of the cluster to terminate
        api_key: API key for authentication
        
    Returns:
        Empty response on success
        
    Raises:
        HTTPException: If the API request fails
    """
    try:
        response = await clusters.terminate_cluster(cluster_id)
        return format_response(success=True, data=response)
    except DatabricksAPIError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/list",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="List all clusters",
    description="List all Databricks clusters.",
)
async def list_clusters(
    api_key: Dict[str, Any] = Depends(validate_api_key),
) -> Dict[str, Any]:
    """
    List all Databricks clusters.
    
    Args:
        api_key: API key for authentication
        
    Returns:
        Response containing a list of clusters
        
    Raises:
        HTTPException: If the API request fails
    """
    try:
        response = await clusters.list_clusters()
        return format_response(success=True, data=response)
    except DatabricksAPIError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/{cluster_id}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get cluster information",
    description="Get information about a specific Databricks cluster.",
)
async def get_cluster(
    cluster_id: str = Path(..., description="Cluster ID"),
    api_key: Dict[str, Any] = Depends(validate_api_key),
) -> Dict[str, Any]:
    """
    Get information about a specific cluster.
    
    Args:
        cluster_id: ID of the cluster
        api_key: API key for authentication
        
    Returns:
        Response containing cluster information
        
    Raises:
        HTTPException: If the API request fails
    """
    try:
        response = await clusters.get_cluster(cluster_id)
        return format_response(success=True, data=response)
    except DatabricksAPIError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/start",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Start a cluster",
    description="Start a terminated Databricks cluster.",
)
async def start_cluster(
    cluster_id: str,
    api_key: Dict[str, Any] = Depends(validate_api_key),
) -> Dict[str, Any]:
    """
    Start a terminated Databricks cluster.
    
    Args:
        cluster_id: ID of the cluster to start
        api_key: API key for authentication
        
    Returns:
        Empty response on success
        
    Raises:
        HTTPException: If the API request fails
    """
    try:
        response = await clusters.start_cluster(cluster_id)
        return format_response(success=True, data=response)
    except DatabricksAPIError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/resize",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Resize a cluster",
    description="Resize a Databricks cluster by changing the number of workers.",
)
async def resize_cluster(
    cluster_id: str,
    num_workers: int,
    api_key: Dict[str, Any] = Depends(validate_api_key),
) -> Dict[str, Any]:
    """
    Resize a cluster by changing the number of workers.
    
    Args:
        cluster_id: ID of the cluster to resize
        num_workers: New number of workers
        api_key: API key for authentication
        
    Returns:
        Empty response on success
        
    Raises:
        HTTPException: If the API request fails
    """
    try:
        response = await clusters.resize_cluster(cluster_id, num_workers)
        return format_response(success=True, data=response)
    except DatabricksAPIError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/restart",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Restart a cluster",
    description="Restart a Databricks cluster.",
)
async def restart_cluster(
    cluster_id: str,
    api_key: Dict[str, Any] = Depends(validate_api_key),
) -> Dict[str, Any]:
    """
    Restart a Databricks cluster.
    
    Args:
        cluster_id: ID of the cluster to restart
        api_key: API key for authentication
        
    Returns:
        Empty response on success
        
    Raises:
        HTTPException: If the API request fails
    """
    try:
        response = await clusters.restart_cluster(cluster_id)
        return format_response(success=True, data=response)
    except DatabricksAPIError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) 