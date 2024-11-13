import Cookies from 'js-cookie';

export function clearAllCookies() {
    // Получаем все куки
    const allCookies = Cookies.get();

    // Удаляем каждый куки, проходя по всем ключам
    for (let cookie in allCookies) {
        Cookies.remove(cookie, { path: '/', domain: 'localhost' });
    }

    console.log("Attempted to clear all cookies.");
}

export function useCookies() {
    const setProjectId = (projectId) => {
        Cookies.set('projectId', projectId, { expires: 1 }); // Устанавливаем куку на 7 дней
    };

    const getProjectId = () => {
        return Cookies.get('projectId');
    };

    const setUserName = (userName) => {
        Cookies.set('userName', userName, { expires: 1 }); // Устанавливаем куку на 7 дней
    };

    const getUserName = () => {
        return Cookies.get('userName');
    };

    const setProjectName = (projectName) => {
        Cookies.set('projectName', projectName, { expires: 1 }); // Устанавливаем куку на 7 дней
    };

    const getProjectName = () => {
        return Cookies.get('projectName');
    };

    const setStageName = (stageName) => {
        Cookies.set('stageName', stageName, { expires: 1 }); // Устанавливаем куку на 7 дней
    };

    const getStageName = () => {
        return Cookies.get('stageName');
    };

    const setStageId = (stageId) => {
        Cookies.set('stageId', stageId, { expires: 1 }); // Устанавливаем куку на 7 дней
    };

    const getStageId = () => {
        return Cookies.get('stageId');
    };
    const setTaskId = (taskId) => {
        Cookies.set('taskId', taskId, { expires: 1 }); // Устанавливаем куку на 7 дней
    };

    const getTaskId = () => {
        return Cookies.get('taskId');
    };
    const setRiskId = (riskId) => {
        Cookies.set('riskId', riskId, { expires: 1 }); // Устанавливаем куку на 7 дней
    };

    const getRiskId = () => {
        return Cookies.get('riskId');
    };

    const setReceiverId = (receiverId) => {
        Cookies.set('receiverId', receiverId, { expires: 1 }); // Устанавливаем куку на 7 дней
    };

    const getReceiverId = () => {
        return Cookies.get('receiverId');
    };

    const setReceiverName = (receiverName) => {
        Cookies.set('receiverName', receiverName, { expires: 1 }); // Устанавливаем куку на 7 дней
    };

    const getReceiverName = () => {
        return Cookies.get('receiverName');
    };

    return {
        setProjectId,
        getProjectId,
        setUserName,
        getProjectName,
        setProjectName,
        getUserName,
        setStageName,
        getStageName,
        setStageId,
        getStageId,
        getTaskId,
        setTaskId,
        getRiskId,
        setRiskId,
        setReceiverId,
        getReceiverId,
        setReceiverName,
        getReceiverName,
    };
}
